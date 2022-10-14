"""
CLI Command Extensions for Flask
"""
from unittest import TestCase
from unittest.mock import patch, MagicMock
from click.testing import CliRunner
from service.common.cli_commands import db_create
from service import app
from service.models import db

class TestFlaskCLI(TestCase):
    """Test Flask CLI Commands"""

    def setUp(self):
        self.runner = CliRunner()

    @patch('service.common.cli_commands.db')
    def test_db_create(self, db_mock):
        """It should call the db-create command"""
        db_mock.return_value = MagicMock()
        result = self.runner.invoke(db_create)
        self.assertEqual(result.exit_code, 0)


######################################################################
# Command to force tables to be rebuilt
# Usage: flask create-db
######################################################################
@app.cli.command("create-db")
def create_db():
    """
    Recreates a local database. You probably should not use this on
    production.
    """
    db.drop_all()
    db.create_all()
    db.session.commit()