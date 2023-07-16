from pathlib import Path


def delete_files(file_name):
    # Указываем путь к директории
    directory = Path('static/docs_template')
    file_path = directory / file_name

    # Проверяем, существует ли файл
    if file_path.is_file():
        # Удаляем файл
        file_path.unlink()
        print(f"Файл '{file_name}' удален успешно.")
    else:
        print(f"Файл '{file_name}' не существует.")


delete_files('chenge.docx')
