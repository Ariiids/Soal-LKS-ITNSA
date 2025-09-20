import enum
import re
from nornir.core.task import Task
from tasks.common.command_controller import run_command

from tasks.common.helper import UNKNOWN_MSG, process_result_exit_code
from tasks.common.sub_aspect_model import SubAspectResult

BASE_DN = "dc=int,dc=worldskills,dc=org"
ADMIN_DN = "cn=admin,dc=int,dc=worldskills,dc=org"
ADMIN_PW = "Skill39@Lyon"


class LDAP_ATTR(enum.StrEnum):
    MAIL_EXISTS = "mail"
    OU_EXISTS = "ou"
    UID_EXISTS = "uid"
    CN_EXISTS = "cn"
    LOGIN_FAILED = "login"


def get_ldap_user_base_search(username: str) -> str:
    if username == "admin":
        return f'ldapsearch -H ldap://localhost -b cn={username},{BASE_DN} -x "(objectclass=*)"'
    return f'ldapsearch -H ldap://localhost -b {BASE_DN} -x "(&(objectclass=person)(uid={username}))"'


def get_ldap_user_search(username: str) -> str:
    base_command = get_ldap_user_base_search(username=username)
    command_with_user = f"{base_command} -D {ADMIN_DN} -w {ADMIN_PW}"
    command = f"({command_with_user} || {base_command}) 2>&1"
    return command


def check_ldap_user_exists(task: Task, username: str) -> SubAspectResult:
    command = get_ldap_user_search(username=username)

    score = 0
    cmd_result = None
    msg = f"User {username} DOES NOT exists"
    try:
        cmd_result = run_command(task=task, command=command)
        if username != "admin" and f"uid: {username}" in cmd_result.result:
            msg = f"User {username} exists"
            score = 1
        if username == "admin" and f"dn: cn={username},{BASE_DN}" in cmd_result.result:
            msg = f"User {username} exists"
            score = 1
    except Exception:
        score = 0

    return {
        "command": command,
        "msg": msg,
        "score": score,
        "command_output": cmd_result.result if cmd_result else UNKNOWN_MSG,
    }


def check_ldap_user_attributes(task: Task, username: str, mail: str) -> SubAspectResult:
    """check ldap user attributes"""
    command = get_ldap_user_search(username=username)

    missing_attr = []
    score = 0
    cmd_result = None
    try:
        # Redirect stderr to stdout
        cmd_result = run_command(task=task, command=command)
        # Check if ou exits
        if f"uid: {username}" not in cmd_result.result:
            missing_attr.append(LDAP_ATTR.UID_EXISTS)

        # Mail attribute is set
        if f"mail: {mail}" not in cmd_result.result:
            missing_attr.append(LDAP_ATTR.MAIL_EXISTS)

        # member of OU Employees
        if "ou=Employees,dc=int,dc=worldskills,dc=org" not in cmd_result.result:
            missing_attr.append(LDAP_ATTR.OU_EXISTS)
        
        if len(missing_attr) == 0:
            score = 1
    except Exception:
        pass


    # Prepare message
    msg = f"User {username} DOES NOT exists"
    if score == 0:
        msg = f"User {username} exists, but attributes are missing: {', '.join(missing_attr)}"
    else:
        msg = f"User {username} has correct attributes"

    return {
        "command": command,
        "msg": msg,
        "score": score,
        "command_output": cmd_result.result if cmd_result else UNKNOWN_MSG,
    }


def check_ldap_login(task: Task, username: str):
    """LDAP user login"""
    base_command = get_ldap_user_base_search(username=username)
    command = get_ldap_user_search(username=username)
    cn = ""
    score = 0
    commands = [command]
    command_outputs = []
    try:
        # Redirect stderr to stdout
        cmd_result = run_command(task=task, command=command)
        command_outputs.append(cmd_result.result)

        # Get configured DN for the user
        re_cn = re.findall(r"^dn: (.*)$", str(cmd_result.result), re.MULTILINE)
        if len(re_cn) > 0:
            cn = re_cn[0]
    except Exception:
        command_outputs.append(UNKNOWN_MSG)

    if cn:
        # Try to login
        login_command = f"{base_command} -D \"{cn}\" -w {ADMIN_PW}"
        commands.append(login_command)
        try:
            run_command(task=task, command=f"{login_command}")
            score = 1
            command_outputs.append(process_result_exit_code(True))
        except Exception:
            command_outputs.append(process_result_exit_code(False))
    # Prepare message
    if score == 0:
        msg = f"User {username} cannot login"
    else:
        msg = f"User {username} can login"

    return {
        "command": commands,
        "msg": msg,
        "score": score,
        "command_output": command_outputs,
    }
