import openstack
from flask import Flask, jsonify


conn = openstack.connect(cloud='xerces')
CONTAINER = "visits"
OBJECT = "counter.txt"

def ensure_container(name: str):
    containers = [container.name for container in conn.object_store.containers()]
    if name not in containers:
        conn.object_store.create_container(name=name)
    
def ensure_object(container: str, obj: str, default_text: str = "0"):
    objects = [container_obj.name for container_obj in conn.object_store.objects(container)]
    if obj not in objects:
        conn.object_store.upload_object(
            container=container,
            name=obj,
            data=default_text
        )

def read_count():
    response = conn.object_store.download_object(container=CONTAINER, obj=OBJECT)
    content = bytes(response)
    print(content.decode('utf-8'))
    return int(content.decode('utf-8'))

def write_count(count):
    conn.object_store.upload_object(
        container=CONTAINER,
        name=OBJECT,
        data=str(count),
        content_type='text/plain'
    )

# initialization
ensure_container(CONTAINER)
ensure_object(CONTAINER, OBJECT, "0")

app = Flask(__name__)

@app.route("/")
def handle_get(): 
    count = read_count()
    count += 1
    write_count(count)
    return jsonify(value=count)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

