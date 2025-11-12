from typing import Optional, Dict, Any, Union
import httpx
from mcp.server.fastmcp import FastMCP, Context
import subprocess, os, time
import requests
import json
import time
import re
import asyncio

# Disable SSL warnings
requests.packages.urllib3.disable_warnings()

# Initialize FastMCP server
mcp = FastMCP("BOSH-MCP", host="0.0.0.0", port=8080)



async def execute_shell_cmd(cmd: str, remove_esc: bool = False) -> tuple[int, str]:

    msg = ''
    my_env = os.environ.copy()

    proc = subprocess.Popen(f'{cmd} 2>&1',  shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=my_env, text=True )

    print(f"Executing CMD: {cmd}")
    # Create async tasks to read stdout
    async def read_stream(stream):
        output = []
        msg = ''
        while True:
            line = await asyncio.get_event_loop().run_in_executor(None, stream.readline)
            if not line:
                break
            print(line)
            #output.append(line)
            msg += line
        #return ''.join(output)
        return msg
    
    # Run the tasks concurrently
    stdout = await asyncio.gather(
        read_stream(proc.stdout),
        #read_stream(process.stderr)
    )
    
    # Wait for the process to complete and get the return code
    return_code = await asyncio.get_event_loop().run_in_executor(None, proc.wait)
    print(f"DONE Executing CMD")
    return return_code, stdout



@mcp.tool()
async def bosh_director_login(director: str, username: str, password: str ) -> str:
    """Log into a BOSH Director.

    Args:
        director: The FQDN or IP address of the BOSH Director
        username: The username
        password: The password
    """
    
    bosh_alias_cmd = f'src/bosh-alias-create.sh {director} {director}'

    ret_code, msg = await execute_shell_cmd(bosh_alias_cmd)
    
    if ret_code != 0:
        msg = f"return code:\r\n{ret_code}\r\n\r\n" + f"Output:\r\n\r\nError - Either director is invalid or inaccessible"
        return msg

    bosh_login_cmd = f'src/bosh-login.exp {director} {username} {password}'

    ret_code, msg = await execute_shell_cmd(bosh_login_cmd)

    msg = f"bosh log-in return code:\r\n{ret_code}\r\n\r\n" + f"bosh log-in output:\r\n\r\n{msg}"
    return msg    


@mcp.tool()
async def execute_bosh_cmd(bosh_cmd: str) -> str:
    """Execute a bosh cmd on a bosh director.  Always specify bosh -e <director> in your cmd.
    If this command returns a login or authentication error
    call bosh_director_login to log into the bosh director.

    Args:
        bosh_cmd: bosh cmd
    """

    # tuple of bosh commands that are not permitted
    disallowed = ()

    bosh_cmd_stripped = bosh_cmd.lstrip()

    # Make sure bosh_cmd starts with bosh
    if not bosh_cmd_stripped.lower().startswith("bosh"):
        return f"Error: Only bosh commands are permitted"

    # Make sure disallowed bosh commands are not executed
    for disallowed_str in disallowed:
        
        if bosh_cmd_stripped.lower().find(disallowed_str) != -1:
            return f"Error: {disallowed_str} commands are not permitted"
        

    ret_code, msg = await execute_shell_cmd(bosh_cmd)

    msg = f"bosh cmd return code:\r\n{ret_code}\r\n\r\n" + f"bosh cmd output:\r\n\r\n{msg}"

    return msg


def main():
    mcp.run(transport='sse')


if __name__ == "__main__":
    main()