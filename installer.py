#!/usr/bin/env python3
import os
import sys
from pathlib import Path


def check_python_version():
    """Проверяет, что Python >= 3.12."""
    if sys.version_info < (3, 12):
        print(f"❌ Нужен Python 3.12 или выше. У тебя: {sys.version.split()[0]}")
        sys.exit(1)


def get_bin_dir():
    """Возвращает директорию для пользовательских бинарников."""
    # ~/.local/bin — стандарт XDG Base Directory
    bin_dir = Path.home() / ".local" / "bin"
    bin_dir.mkdir(parents=True, exist_ok=True)
    return bin_dir


def install():
    check_python_version()

    # Путь к исходному скрипту create-flask
    script_path = Path(__file__).resolve().parent / "create-flask"

    if not script_path.exists():
        print(f"❌ Не найден файл: {script_path}")
        print("   Убедись, что installer.py лежит рядом с create-flask.")
        sys.exit(1)

    # Куда ставим симлинк
    bin_dir = get_bin_dir()
    link_path = bin_dir / "create-flask"

    # Если уже что-то есть — убираем
    if link_path.exists() or link_path.is_symlink():
        try:
            link_path.unlink()
            print(f"♻️  Удалён старый симлинк: {link_path}")
        except OSError as e:
            print(f"❌ Не удалось удалить старый симлинк: {e}")
            sys.exit(1)

    # Создаём симлинк
    try:
        link_path.symlink_to(script_path)
    except OSError as e:
        print(f"❌ Не удалось создать симлинк: {e}")
        sys.exit(1)

    # Делаем исполняемым
    try:
        script_path.chmod(0o755)
    except OSError:
        pass  # не критично, но лучше попытаться

    print(f"✅ Установлено: {link_path} -> {script_path}")

    # Проверяем PATH
    path_env = os.environ.get("PATH", "")
    bin_dir_str = str(bin_dir)

    if bin_dir_str not in path_env.split(os.pathsep):
        print()
        print("⚠️  Директория ~/.local/bin НЕ в PATH.")
        print("   Добавь в ~/.zshrc (macOS) или ~/.bashrc (Linux):")
        print()
        print(f'   export PATH="{bin_dir_str}:$PATH"')
        print()
        print("   Затем перезапусти терминал или выполни:")
        print(f'   source ~/.zshrc   # или source ~/.bashrc')
    else:
        print("✅ ~/.local/bin уже в PATH. Можно пользоваться:")
        print("   create-flask")


if __name__ == "__main__":
    install()
