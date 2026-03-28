import sys

# Prepend the dependencies folder to Python's import path
sys.path.insert(0, '/app/deps')

import streamlit.web.cli

if __name__ == '__main__':
    # Construct the arguments to run the streamlit app
    sys.argv = [
        'streamlit',
        'run', 'main.py',
        '--server.port', '8080',
        '--server.address', '0.0.0.0',
        '--server.headless', 'true',
        '--server.enableCORS', 'false'
    ]
    # Launch Streamlit
    sys.exit(streamlit.web.cli.main())
