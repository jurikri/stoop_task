  import subprocess
    import pkg_resources
    
    def install_package(package_name):
        # 패키지가 이미 설치되어 있는지 확인
        installed_packages = {pkg.key for pkg in pkg_resources.working_set}
        if package_name not in installed_packages:
            # 패키지가 설치되어 있지 않을 경우 설치
            subprocess.check_call(["python", "-m", "pip", "install", package_name])
            print(f"{package_name} has been installed.")
        else:
            # 패키지가 이미 설치되어 있음
            print(f"{package_name} is already installed.")
    
    # 패키지 이름 설정
    package_names = ['python-binance', 'forex-python', 'matplotlib', 'tqdm']
    for package_name in package_names:
        install_package(package_name)
