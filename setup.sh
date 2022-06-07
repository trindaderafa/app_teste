mkdir -p ~/.streamlit

echo "[server]
headless = true
port = $PORT
enableCORS = false
[theme]
base = 'light'
primaryColor = '#194ad7'
backgroundColor = '#ecf4fb'
[mapbox]
token = 'pk.eyJ1IjoiYXBwaW1tb3ZpIiwiYSI6ImNsMzR6eXg4djE4bjMzanJ4NzVic2Nmb3EifQ.HgHvze4WT9SB9WYG6GTZmg'
" > ~/.streamlit/config.toml
