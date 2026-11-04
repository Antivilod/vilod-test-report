# Vilod Test Report

Create a standalone, printable HTML defect report from structured JSON.
Useful for a small QA handoff when a full issue tracker is unnecessary.

## Example

`python report.py example.json demo-report.html`

Open demo-report.html in a browser. The output file must not already exist.
Required top-level fields: title (string), defects (array). Every defect needs
id, title, severity, expected and actual (strings), and steps (array of strings).
All user text is HTML-escaped. The report has no scripts or remote resources.
Screenshot attachments and automatic data import are not implemented.
Exit code 0 means success, 2 means input, schema or output error.

## По-русски

Локальное создание HTML-отчета с дефектами, шагами, ожидаемым и фактическим
результатом. Пример содержит только вымышленные данные. Исходный JSON не меняется.

## Requirements and status

Python 3.10+, standard library only. Source preview 0.2.0. No installation
of external packages is required. Linux tests passed; Windows is not yet verified.
No network calls, telemetry or accounts. Input content is not anonymized.
Review reports before sharing. No EXE or graphical interface is included.

## Testing

From this tool folder: `python -m unittest discover -v`.
On Windows use `py` instead of `python` if required.

## License

MIT. Copyright (c) 2026 Vilod. See LICENSE.

## Download and run

Use GitHub Code > Download ZIP, extract it, and run the commands above from the extracted folder. The download contains Python source, not an installer. Keep real input files and generated reports outside the repository.

## Скачать и запустить

Нажмите Code > Download ZIP, распакуйте архив и откройте терминал в папке программы. Нужен Python 3.10 или новее. Команды выше запускаются без установки сторонних библиотек. Это исходники, не EXE-установщик.

## Environment and status in 0.2.0

The optional top-level `environment` object contains string keys and string values, for example `{"Application":"Demo 1.0","Platform":"Test environment"}`. Each defect can have `status`: `open`, `in_progress`, `fixed` or `closed`. Missing status defaults to `open`, preserving older JSON input. The HTML shows an environment section and counts by status. Eight unit tests passed on Linux.

Можно указать окружение проверки и статус каждого дефекта. Все эти поля попадают в отчёт, поэтому не добавляйте имя пользователя, личные пути, адреса или секреты. Значения экранируются для HTML, но не обезличиваются.
