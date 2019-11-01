from cx_Freeze import setup, Executable

includefiles = ['templates/', 'static/', 'flask_config.py']

base = None

main_executable = Executable("app.py", base=base, targetName="TGD Kiosk.exe")

setup(name="TGDKisok",
      version="1.1",
      description="TGDKiosk",
      options={
      'build_exe': {
          'namespace_packages': ['ruamel.yaml'],
          'packages': ['jinja2',
                       'jinja2.ext',
                       'flask_wtf',
                       'os'],
          'includes': ['PyQt5'],
          'include_files': includefiles,
          'include_msvcr': True}},
      executables=[main_executable], requires=['flask', 'wtforms'])