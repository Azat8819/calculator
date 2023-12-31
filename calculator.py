import io
import sys
import wave
from io import BytesIO
from typing import Union, Optional
from speechkit import Session, SpeechSynthesis

from pyaudio import PyAudio, paInt16
from PyQt5.QtWidgets import QApplication, QMainWindow

from design import Ui_MainWindow
# import ui.files_rc
import config


class Calculator(QMainWindow):
    oauth_token = "y0_AgAAAAA0ACvDAATuwQAAAADxeyLXKispk9SRR9e47bP-kqxd-HKe2fA"
    catalog_id = "b1gchocvafu3ogkejftd"
    record_status = False
    session = Session.from_yandex_passport_oauth_token(oauth_token, catalog_id)
    synthesizeAudio = SpeechSynthesis(session)

    def __init__(self):
        super(Calculator, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.entry = self.ui.le_entry
        self.temp = self.ui.lbl_temp
        self.entry_max_len = self.entry.maxLength()

        self.connect_digit_buttons()
        self.connect_math_operations()
        self.connect_other_buttons()
        self.connect_voice_buttons()

        self.entry.textChanged.connect(self.adjust_entry_font_size)
        # self.temp.textChanged.connect(self.adjust_temp_font_size)

    def connect_digit_buttons(self) -> None:
        for btn in config.DIGIT_BUTTONS:
            getattr(self.ui, btn).clicked.connect(self.add_digit)

    def connect_math_operations(self) -> None:
        self.ui.btn_calc.clicked.connect(self.calculate)
        for btn in config.MATH_OPERATIONS:
            getattr(self.ui, btn).clicked.connect(self.math_operation)

    def connect_other_buttons(self) -> None:
        self.ui.btn_clear.clicked.connect(self.clear_all)
        self.ui.btn_point.clicked.connect(self.add_point)
        self.ui.btn_neg.clicked.connect(self.negate)
        self.ui.btn_percent.clicked.connect(self.percent)

    def connect_voice_buttons(self) -> None:
        self.ui.btn_record.clicked.connect(self.record)

    def add_digit(self) -> None:
        self.remove_error()
        self.clear_temp_if_equality()
        btn = self.sender()

        if btn.objectName() in config.DIGIT_BUTTONS:
            if self.entry.text() == '0':
                self.entry.setText(btn.text())
            else:
                self.entry.setText(self.entry.text() + btn.text())

    def add_point(self) -> None:
        self.clear_temp_if_equality()
        if '.' not in self.entry.text():
            self.entry.setText(self.entry.text() + '.')

    def avoid_deleting_char_on_negation(self, entry: str) -> None:
        if len(entry) == self.entry_max_len + 1 and '-' in entry:
            self.entry.setMaxLength(self.entry_max_len + 1)
        else:
            self.entry.setMaxLength(self.entry_max_len)

    def negate(self) -> None:
        self.clear_temp_if_equality()
        entry = self.entry.text()

        if '-' not in entry:
            if entry != '0':
                entry = '-' + entry
        else:
            entry = entry[1:]

        self.avoid_deleting_char_on_negation(entry)
        self.entry.setText(entry)

    def percent(self) -> None:
        self.remove_error()
        self.clear_temp_if_equality()
        entry = self.remove_trailing_zeros(self.entry.text())
        if entry != '0':
            result = float(entry) / 100
            if result.is_integer():
                result = int(result)
            self.entry.setText(self.remove_trailing_zeros(str(result)))

    def clear_all(self) -> None:
        self.remove_error()
        self.entry.setText('0')
        self.temp.clear()

    def clear_entry(self) -> None:
        self.remove_error()
        self.clear_temp_if_equality()
        self.entry.setText('0')

    def clear_temp_if_equality(self) -> None:
        if self.get_math_sign() == '=':
            self.temp.clear()

    @staticmethod
    def remove_trailing_zeros(num: Union[float, int, str]) -> str:
        n = str(float(num))
        return n.replace('.0', '') if n.endswith('.0') else n

    def add_temp(self) -> None:
        btn = self.sender()
        entry = self.remove_trailing_zeros(self.entry.text())

        if not self.temp.text() or self.get_math_sign() == '=':
            self.temp.setText(entry + f' {btn.text()} ')
            self.entry.setText('0')

    def get_entry_num(self) -> Union[int, float]:
        entry = self.entry.text().strip('.')
        return float(entry) if '.' in entry else int(entry)

    def get_temp_num(self) -> Union[int, float, None]:
        if self.temp.text():
            temp = self.temp.text().strip('.').split()[0]
            return float(temp) if '.' in temp else int(temp)

    def get_math_sign(self) -> Optional[str]:
        if self.temp.text():
            return self.temp.text().strip('.').split()[-1]

    def get_entry_text_width(self) -> int:
        return self.entry.fontMetrics().boundingRect(self.entry.text()).width()

    def get_temp_text_width(self) -> int:
        return self.temp.fontMetrics().boundingRect(self.temp.text()).width()

    def calculate(self) -> Optional[str]:
        try:
            result = self.remove_trailing_zeros(
                (config.OPERATIONS[self.get_math_sign()](
                    self.get_temp_num(), self.get_entry_num())))

            self.temp.setText(self.temp.text() +
                              self.remove_trailing_zeros(self.entry.text()) + ' =')

            self.entry.setText(result)

            return result

        except KeyError:
            pass
        except ZeroDivisionError:
            self.show_zero_division_error()

    def show_zero_division_error(self) -> None:
        if self.get_temp_num() == 0:
            self.show_error(config.ERROR_UNDEFINED)
        else:
            self.show_error(config.ERROR_ZERO_DIV)

    def math_operation(self) -> None:
        btn = self.sender()

        if not self.temp.text():
            self.add_temp()
        else:
            if self.get_math_sign() != btn.text():
                if self.get_math_sign() == '=':
                    self.add_temp()
                else:
                    self.replace_temp_sign()
            else:
                try:
                    self.temp.setText(self.calculate() + f' {btn.text()} ')
                except TypeError:
                    pass

    def replace_temp_sign(self) -> None:
        btn = self.sender()
        self.temp.setText(self.temp.text()[:-2] + f'{btn.text()} ')

    def show_error(self, text: str) -> None:
        self.entry.setMaxLength(len(text))
        self.entry.setText(text)
        self.disable_buttons(True)

    def remove_error(self) -> None:
        if self.entry.text() in (config.ERROR_UNDEFINED, config.ERROR_ZERO_DIV):
            self.entry.setMaxLength(self.entry_max_len)
            self.entry.setText('0')
            self.disable_buttons(False)

    def disable_buttons(self, disable: bool) -> None:
        for btn in config.BUTTONS_TO_DISABLE:
            getattr(self.ui, btn).setDisabled(disable)

        color = 'color: #888;' if disable else 'color: white;'
        self.change_buttons_color(color)

    def change_buttons_color(self, css_color: str) -> None:
        for btn in config.BUTTONS_TO_DISABLE:
            getattr(self.ui, btn).setStyleSheet(css_color)

    def adjust_entry_font_size(self) -> None:
        font_size = config.DEFAULT_ENTRY_FONT_SIZE
        while self.get_entry_text_width() > self.entry.width() - 15:
            font_size -= 1
            self.entry.setStyleSheet(f'font-size: {font_size}pt; border: none;')

        font_size = 1
        while self.get_entry_text_width() < self.entry.width() - 60:
            font_size += 1

            if font_size > config.DEFAULT_ENTRY_FONT_SIZE:
                break

            self.entry.setStyleSheet(f'font-size: {font_size}pt; border: none;')

    def adjust_temp_font_size(self) -> None:
        font_size = config.DEFAULT_FONT_SIZE
        while self.get_temp_text_width() > self.temp.width() - 10:
            font_size -= 1
            self.temp.setStyleSheet(f'font-size: {font_size}pt; color: #888;')

        font_size = 1
        while self.get_temp_text_width() < self.temp.width() - 60:
            font_size += 1

            if font_size > config.DEFAULT_FONT_SIZE:
                break

            self.temp.setStyleSheet(f'font-size: {font_size}pt; color: #888;')

    def record(self) -> None:
        self.record_status = not self.record_status
        if self.record_status:
            self.ui.btn_record.setText("Подсчёт")
            self.record_and_recognize()
            self.ui.btn_record.setText("Запись")
            self.record_status = not self.record_status
        else:
            return

    def record_and_recognize(self) -> None:
        data = self.record_audio()

        # Отправляем на распознавание
        text = self.recognizeShortAudio.recognize(
            data, format='lpcm', sampleRateHertz=config.sample_rate)
        print(text)

    @staticmethod
    def record_audio() -> BytesIO:
        """
        Записывает аудио данной продолжительности и возвращает бинарный объект с данными
        """

        p = PyAudio()
        stream = p.open(
            format=paInt16,
            channels=config.num_channels,
            rate=config.sample_rate,
            input=True,
            frames_per_buffer=config.chunk_size
        )
        frames = []
        try:
            for i in range(0, int(config.sample_rate / config.chunk_size * config.seconds)):
                data = stream.read(config.chunk_size)
                frames.append(data)
        finally:
            stream.stop_stream()
            stream.close()
            p.terminate()

        container = io.BytesIO()
        wf = wave.open(container, 'wb')
        wf.setnchannels(config.num_channels)
        wf.setsampwidth(p.get_sample_size(paInt16))
        wf.setframerate(config.sample_rate)
        wf.writeframes(b''.join(frames))
        container.seek(0)
        return container

    def resizeEvent(self, event) -> None:
        self.adjust_entry_font_size()
        self.adjust_temp_font_size()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = Calculator()
    window.show()

    sys.exit(app.exec())
