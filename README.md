# Introduction - The API Monitor

This is an API project for monitoring Photovoltaic Plants. With the objective of demonstrating, through the Python language, CRUD's, endpoints that are related to terms and data of Plants, Inverters, Metrics, Generation, etc.

---

## Tecnologies

- [x] Python
- [x] FastAPI
- [x] Uvicorn
- [x] HTTP Requests
- [x] Docker

---

## Instalation and use

- Clone the project and access the directory:

```bash
git clone https://github.com/LudmilaY/API-monitor.git
cd API-monitor
```
- Create a virtual environment and activate it:

```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate
```

- Install the dependencies:

```bash
pip install -r requirements.txt
```

### Running with Docker

- If you prefer, you can run the project in a container with Docker:

```bash
docker build -t api-monitor .
```

- Execute the container:

```bash
docker run -d -p 8000:8000 api-monitor
```

- Access on browser:

```bash
http://localhost:8000
```

### Running manually

- If you choose to run manually, use the terminal on the path of the source code and run:

```bash
uvicorn main:app --reload
```

- You'll see something like this:
![uvicorn_run](https://github.com/user-attachments/assets/4086e361-e623-47c1-b397-1843bca73b17)

- You can run the application on:

```bash
http://127.0.0.1:8000/docs#/
```
### Expected screens

This first image demonstrates what it looks like on the application screen on the browser:

![screen_app_try](https://github.com/user-attachments/assets/807c7b3e-f331-47c5-b235-d3b2546ea97c)

To run experiments, you can click on the "Try it out" button on the image above. Then you can enter the data you want to search as seen on the image below:

![screen_app_example](https://github.com/user-attachments/assets/8170e148-9596-4d35-b572-a7cb4aed25e3)

## Conclusions

Thanks for your reading, and if you want to reach out you can find me on my [LinkedIn](https://br.linkedin.com/in/ludmila-yung-167ba1b0).
