import os
import subprocess
import requests
from urllib.parse import urljoin

from subjective_abstract_data_source_package import SubjectiveDataSource
from brainboost_data_source_logger_package.BBLogger import BBLogger
from brainboost_configuration_package.BBConfig import BBConfig


class SubjectiveMercurialDataSource(SubjectiveDataSource):
    def __init__(self, name=None, session=None, dependency_data_sources=[], subscribers=None, params=None):
        super().__init__(name=name, session=session, dependency_data_sources=dependency_data_sources, subscribers=subscribers, params=params)
        self.params = params

    def fetch(self):
        repo_url = self.params['repo_url']
        target_directory = self.params['target_directory']

        BBLogger.log(f"Starting fetch process for Mercurial repository '{repo_url}' into directory '{target_directory}'.")

        if not os.path.exists(target_directory):
            try:
                os.makedirs(target_directory)
                BBLogger.log(f"Created directory: {target_directory}")
            except OSError as e:
                BBLogger.log(f"Failed to create directory '{target_directory}': {e}")
                raise

        try:
            subprocess.run(['hg', 'clone', repo_url, target_directory], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            BBLogger.log("Successfully cloned Mercurial repository.")
        except subprocess.CalledProcessError as e:
            BBLogger.log(f"Error cloning Mercurial repository: {e.stderr.decode().strip()}")
        except Exception as e:
            BBLogger.log(f"Unexpected error cloning Mercurial repository: {e}")
    
    # ------------------------------------------------------------------
    def get_icon(self):
        """Return SVG icon content, preferring a local icon.svg in the plugin folder."""
        icon_path = os.path.join(os.path.dirname(__file__), 'icon.svg')
        try:
            if os.path.exists(icon_path):
                with open(icon_path, 'r', encoding='utf-8') as f:
                    return f.read()
        except Exception:
            pass
        return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><rect width="24" height="24" rx="4" fill="#1b1b1b"/><path fill="#bfbfbf" d="M5 7h14v2H5zm0 4h12v2H5zm0 4h8v2H5z"/></svg>'

    def get_connection_data(self):
        """
        Return the connection type and required fields for Mercurial.
        """
        return {
            "connection_type": "Mercurial",
            "fields": ["repo_url", "target_directory"]
        }

