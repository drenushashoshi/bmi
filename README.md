# BMI Calculator — Streamlit Cloud + MongoDB

Small Streamlit app: enter **name, height, weight** → it shows **name, height, weight, BMI (+ category)** and saves every calculation to **MongoDB Atlas**.

## Run locally

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Put your MongoDB connection string in `.streamlit/secrets.toml`:
   ```toml
   [mongo]
   uri = "mongodb+srv://<username>:<password>@<cluster>.mongodb.net/?retryWrites=true&w=majority"
   ```
3. Start the app:
   ```
   streamlit run app.py
   ```

## Set up MongoDB Atlas (free)

1. Create a free account at https://www.mongodb.com/cloud/atlas → create a free **M0 cluster**.
2. **Database Access** → add a database user (username + password).
3. **Network Access** → add IP `0.0.0.0/0` (required so Streamlit Cloud can connect).
4. **Connect → Drivers → Python** → copy the connection string and paste it into your secrets (replace `<username>`/`<password>`).

Data is stored in database `bmi_app`, collection `records`.

## Deploy to Streamlit Cloud

1. Push this folder to a **public GitHub repo** (`app.py`, `requirements.txt`, `.gitignore`, `README.md` — **not** `secrets.toml`).
2. Go to https://share.streamlit.io → **New app** → pick the repo, branch `main`, main file `app.py`.
3. In the app's **Settings → Secrets**, paste:
   ```toml
   [mongo]
   uri = "mongodb+srv://<username>:<password>@<cluster>.mongodb.net/?retryWrites=true&w=majority"
   ```
4. Deploy — every push to `main` redeploys automatically.
