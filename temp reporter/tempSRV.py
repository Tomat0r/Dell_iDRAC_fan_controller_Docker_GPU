from flask import Flask, jsonify
import subprocess

app = Flask(__name__)

def get_gpu_temperatures():
    try:
        output = subprocess.check_output([
            "nvidia-smi",
            "--query-gpu=index,name,temperature.gpu",
            "--format=csv,noheader,nounits"
        ]).decode("utf-8").strip()

        temps = []
        for line in output.split("\n"):
            parts = line.split(",")
            if len(parts) >= 3:
                gpu_index = parts[0].strip()
                gpu_name = parts[1].strip()
                temp = int(parts[2].strip())
                temps.append({
                    "index": gpu_index,
                    "name": gpu_name,
                    "temperature": temp
                })
        return temps
    except Exception as e:
        return {"error": str(e)}

@app.route("/")
def index():
    return jsonify(get_gpu_temperatures())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=680)


