import os
import shutil
import sys
import platform
import subprocess
import tempfile

# Função para criar um arquivo Python que executa o Interface.py
def create_launcher():
    interface_path = os.path.abspath("Interface.py")
    interface_dir = os.path.dirname(interface_path)
    launcher_code = f"""
import os
import subprocess

try:
    subprocess.run(['git', 'pull', 'origin', 'master'], cwd=r'{interface_dir}', check=True)
except Exception:
    pass

os.system(r'python "{interface_path}"')
"""

    with open("launcher.py", "w", encoding="utf-8") as launcher_file:
        launcher_file.write(launcher_code)

# Função para compilar o código em um executável
def compile_to_exe():
    icon_path = os.path.join(os.path.dirname(__file__), "Images", "letter-g.png")
    # Compila diretamente com PyInstaller usando a opção --uac-admin
    subprocess.check_call([
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        f"--icon={icon_path}",
        "--uac-admin",  # Solicitar permissões de administrador
        "launcher.py"
    ])

# Crédito https://sukhbinder.wordpress.com/2023/06/07/simple-python-script-to-create-a-desktop-shortcut/
def create_windows_shortcut_on_desktop(name: str, targetpath: str ):
    SCIPTFILE = """
    Set oWS = WScript.CreateObject("WScript.Shell")
    sLinkFile = "{name}"
    Set oLink = oWS.CreateShortcut(sLinkFile)
    oLink.TargetPath = "{targetpath}"
    oLink.Save
    """

    with tempfile.TemporaryDirectory() as tmpdir:
        bat_file= os.path.join(tmpdir, "CreateShortcut.vbs")
        desktop_loc = os.path.join(os.environ['PUBLIC'], 'Desktop')
        name_path = os.path.join(desktop_loc, "{}.lnk").format(name.upper())
        with open(bat_file, "w") as fout:
            fout.write(SCIPTFILE.format(name=name_path, targetpath=targetpath))
        try:
            subprocess.call(["cscript", bat_file], cwd=tmpdir)
        except Exception as ex:
            print("Error creating shortcut")
            print(ex)

        print("Shortcut link created, check {}".format(desktop_loc))

# Função para mover o executável para a área de trabalho pública
def move_executable():
    src = os.path.join("dist", "launcher.exe" if platform.system() == "Windows" else "launcher")
    dst = os.path.dirname(__file__)
    dst_executable = os.path.join(dst, "launcher.exe" if platform.system() == "Windows" else "launcher")

    # Verifica se o executável já existe e o remove
    if os.path.exists(dst_executable):
        os.remove(dst_executable)

    shutil.move(src, dst)
    create_windows_shortcut_on_desktop('ScrappingImoveis', dst_executable)

# Função para remover a pasta build e o arquivo launcher.py
def cleanup():
    build_path = os.path.join(os.getcwd(), "build")
    dist_path = os.path.join(os.getcwd(), "dist")

    if os.path.exists(build_path):
        shutil.rmtree(build_path)
    if os.path.exists(dist_path):
        shutil.rmtree(dist_path)
    if os.path.exists("launcher.py"):
        os.remove("launcher.py")

# Execução das funções
create_launcher()
compile_to_exe()
move_executable()
cleanup()
