# save file as /opt/yams/qbt.py

# script checks if qbittorrent docker image is running and reloads the docker compose file for yams to restore it if not.
# script is run via crontab for scheduled checks

# crontab
# run 'crontab -e'. Do nto run this as sudo, process will fail if you do
# add "*/15 * * * * python3 /opt/yams/qbt.py >/dev/null 2>&1" to the end of the file to commit it to the cron process.

# script keeps a log of last run/check in the /opt/yams/qbt_log.txt file
# sudo apt install python-pip
# pip install docker

from typing import Optional
import docker
import os
import datetime

runtime = datetime.datetime.now().strftime("%c")

def is_container_running(container_name: str) -> Optional[bool]:
    """Verify the status of a container by it's name

    :param container_name: the name of the container
    :return: boolean or None
    """
    RUNNING = "running"
    docker_client = docker.from_env()

    try:
        container = docker_client.containers.get(container_name)
    except docker.errors.NotFound as exc:
        print(f"Check container name!\n{exc.explanation}")
    else:
        container_state = container.attrs["State"]
        return container_state["Status"] == RUNNING


if __name__ == "__main__":
    container_name = "qbittorrent"
    result = is_container_running(container_name)

    if not result == True:
        file1 = open('/opt/yams/qbt_log.txt', 'w')
        file1.write(f"{runtime} - Container qBittorrent is not running")
        file1.write('\n')
        file1.close()
        os.system("docker-compose -f /opt/yams/docker-compose.yaml up -d --quiet-pull 2>/dev/null")
    else:
        file1 = open('/opt/yams/qbt_log.txt', 'w')
        file1.write(f"{runtime} - Container qBittorrent is running")
        file1.write('\n')
        file1.close()
