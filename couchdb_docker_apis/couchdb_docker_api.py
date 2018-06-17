import time
from docker.errors import NotFound


def run_couchdb_docker_container(docker_client):
    # if there is no image we pull it
    try:
        couchdb_image = docker_client.images.get("couchdb")
    except NotFound as e:
        couchdb_image = docker_client.images.pull("couchdb", tag="latest")

    assert couchdb_image is not None

    # if container is not running we will start it
    try:
        couch_container = docker_client.containers.get("appguard_couch")
        if couch_container.status == "exited" or (couch_container.status == "created"):
            couch_container.remove()
            raise NotFound("Container Exited or could not be started")
    except NotFound as e:
        print("Couch docker container not found or not running\n")
        couch_container = docker_client.containers.run("couchdb",
                                                     name="appguard_couch",
                                                     ports={"5984/tcp": 5984}, detach=True)
        time.sleep(5)

    assert couch_container.status == "running" or (couch_container.status == "created"
                                                 and not couch_container.attrs["State"]["Error"])
    return couch_container