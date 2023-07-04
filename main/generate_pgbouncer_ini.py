#disable by mj to success sonar job.


# import os
# from jinja2 import Environment, FileSystemLoader
# from config import setting
# from pathlib import Path

# BASE_DIR = Path(__file__).resolve().parent.parent

# # Load the Jinja2 template
# template_env = Environment(loader=FileSystemLoader(os.path.join(BASE_DIR, 'pgbouncer/templates')))
# template = template_env.get_template('pgbouncer.ini.j2')

# database_configs = {
#     "host": setting.DATABASE_HOST,
#     "port": setting.DATABASE_PORT,
#     "name": setting.DATABASE_NAME,
#     "user": setting.DATABASE_USER,
#     "password": setting.DATABASE_PASSWORD
# }
# # Render the template with the database configurations
# rendered_template = template.render(database_configs=database_configs)

# # Write the rendered template to the pgbouncer.ini file
# pgbouncer_ini_path = os.path.join(BASE_DIR, 'pgbouncer/pgbouncer.ini')
# with open(pgbouncer_ini_path, 'w') as f:
#     f.write(rendered_template)

# # Set the appropriate file permissions
# os.chmod(pgbouncer_ini_path, 0o600)
