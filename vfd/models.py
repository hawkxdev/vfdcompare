from django.db import models
from supplier.models import Supplier, Brand


class Application(models.Model):
    """
    Области применения частотных преобразователей.

    HVAC, насосы, конвейеры и другие применения.
    """
    name = models.CharField('Наименование', max_length=200, unique=True,
                            help_text='Область применения частотного преобразователя')

    def __str__(self) -> str:
        return str(self.name)

    class Meta:
        verbose_name = 'Применение'
        verbose_name_plural = 'Применения'


class Category(models.Model):
    """
    Категории частотных преобразователей.

    Общепромышленные, специализированные и другие типы VFD.
    """
    name = models.CharField('Наименование', max_length=200, unique=True,
                            help_text='Категория частотного преобразователя')

    def __str__(self) -> str:
        return str(self.name)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Series(models.Model):
    """
    Серии частотных преобразователей от производителей.

    Линейки VFD с общими техническими характеристиками и функциональностью.
    """
    brand = models.ForeignKey(Brand, verbose_name='Бренд', on_delete=models.PROTECT, help_text='Производитель серии')
    name = models.CharField('Название', max_length=200, unique=True, help_text='Название серии')
    category = models.ForeignKey(Category, verbose_name='Категория',
                                 on_delete=models.PROTECT, help_text='Категория применения')
    image = models.ImageField('Картинка', upload_to='images/', blank=True, null=True, help_text='Изображение серии')
    applications = models.ManyToManyField(Application, verbose_name='Применения', help_text='Области применения серии')

    class Power(models.IntegerChoices):
        """Диапазоны мощностей для различных серий VFD"""
        P10 = 10, '1x230В: 0.4...2.2кВт; 3x400В: 0.75...3.7кВт'
        P11 = 11, '1x230В: 0.2...2.2кВт; 3x400В: 0.75...2.2кВт'
        P20 = 20, '1x230В: 0.4...2.2кВт; 3x400В: 0.75...5.5кВт'
        P30 = 30, '1x230В: 0.2...2.2кВт; 3x400В: 0.4...7.5кВт'
        P31 = 31, '3x400В: 0.4...11кВт'
        P40 = 40, '1x230В: 0.4...2.2кВт; 3x400В: 0.75...15кВт'
        P50 = 50, '1x230В: 0.2...2.2кВт; 3x400В: 0.4...22кВт'
        P51 = 51, '1x230В: 0.4...2.2кВт; 3x400В: 0.4...22кВт'
        P60 = 60, '3x400В: 0.75...37кВт'
        P70 = 70, '3x400В: 0.75...90кВт'
        P80 = 80, '1x230В: 0.4...2.2кВт; 3x400В: 0.75...110кВт'
        P90 = 90, '1x230В: 0.4...2.2кВт; 3x400В: 0.75...220кВт'
        P91 = 91, '1x230В: 0.75...2.2кВт; 3x400В: 0.75...220кВт'
        P100 = 100, '3x400В: 0.75...500кВт'
        P101 = 101, '3x400В: 0.75...630кВт'
        P102 = 102, '1x230В: 0.4...2.2кВт; 3x400В: 0.75...630кВт'
        P103 = 103, '1x230В: 0.75...2.2кВт; 3x400В: 0.75...630кВт'
        P104 = 104, '1x230В: 0.2...3.7кВт; 3x400В: 0.75...400кВт'

    power_range = models.PositiveSmallIntegerField(
        verbose_name='Диапазон мощностей',
        choices=Power.choices,
        blank=True,
        null=True,
        help_text='Диапазон мощностей, поддерживаемых серией'
    )

    class ControlMethods(models.IntegerChoices):
        """Методы управления двигателем"""
        C10 = 10, 'V/F (скалярное управление)'
        C20 = 20, 'V/F (скалярное управление), \nSVC (бездатчиковое векторное управление)'
        C30 = 30, 'V/F (скалярное управление), \nSVC (бездатчиковое векторное управление), \n' \
                  'VC (векторное управление с замкнутым контуром)'

    control_methods = models.PositiveSmallIntegerField(
        verbose_name='Методы управления',
        choices=ControlMethods.choices,
        blank=True,
        null=True,
        help_text='Доступные методы управления двигателем'
    )

    class Motors(models.IntegerChoices):
        """Типы поддерживаемых двигателей"""
        F1 = 1, 'IM (асинхронные)'
        F2 = 2, 'IM (асинхронные), PM (синхронные с постоянными магнитами)'
        F3 = 3, 'IM (асинхронные), PM (синхронные с постоянными магнитами), SynRM (синхронные реактивные)'

    motors = models.PositiveSmallIntegerField(
        verbose_name='Двигатели',
        choices=Motors.choices,
        blank=True,
        null=True,
        help_text='Типы двигателей, с которыми может работать серия'
    )

    class MaximumFrequency(models.IntegerChoices):
        """Максимальная выходная частота"""
        F10 = 10, '320'
        F20 = 20, '599; 90 кВт и выше: 400'
        F21 = 21, '500'
        F22 = 22, '400'
        F30 = 30, '599'
        F31 = 31, '600'
        F40 = 40, '999'
        F50 = 50, '3000 (V/F); 300 (SVC)'
        F51 = 51, '3200 (V/F); 300 (SVC)'
        F52 = 52, '3200 (V/F); 500 (SVC)'
        F53 = 53, '5000'

    maximum_output_frequency = models.PositiveSmallIntegerField(
        verbose_name='Максимальная выходная частота, Гц',
        choices=MaximumFrequency.choices,
        blank=True,
        null=True,
        help_text='Максимальная частота выходного сигнала'
    )

    class Overload(models.IntegerChoices):
        """Перегрузочная способность"""
        P10 = 10, 'Лёгкий режим: 120% 60с; \nНормальный режим: 120% 60с, 160% 3с'
        P20 = 20, '150% 60с; 180% 3с'
        P21 = 21, 'G type: 150% 60с, 180% 3с; \nP type: 120% 60с, 150% 3с'
        P22 = 22, '150% 60с; 180% 2с; 200% 0.5c'
        P23 = 23, 'G type: 150% 60с; 180% 3с'
        P24 = 24, '150% 60с каждые 10 мин; 180% 2с'
        P30 = 30, '110% длит.; 150% 60с; 180% 5с'
        P31 = 31, 'Нормальный режим: 120% 60с, 150% 3с; \nТяжелый режим: 150% 60с, 200% 3с'
        P32 = 32, 'G type: 110% длит.; 150% 60с, 200% 4с; \nP type: 105% длит.; 120% 60с, 150% 1с'
        P33 = 33, '150% 60с; 180% 10с; 200% 1c'
        P34 = 34, 'G type: 150% 60с; 180% 10с; 200% 1c; \nP type: 120% 60с'

    overload_capacity = models.PositiveSmallIntegerField(
        verbose_name='Перегрузочная способность',
        choices=Overload.choices,
        blank=True,
        null=True,
        help_text='Способность к кратковременной перегрузке'
    )

    class StartingTorque(models.IntegerChoices):
        """Пусковой момент"""
        S10 = 10, '100% ном. крутящего момента при 5,0Гц (V/F управление); ' \
                  '150% ном. крутящего момента при 1,5Гц (пр. векторное упр.)'
        S20 = 20, '150% / 0.5 Гц'
        S21 = 21, 'G type: 150% / 0.5 Гц (SVC)'
        S22 = 22, 'G type: 150% / 0.5 Гц (SVC);\nP type: 100% / 0.5 Гц'
        S23 = 23, '150% / 3 Гц (V/F), \n150% / 1 Гц (FVC)'
        S24 = 24, '150% / 3 Гц (V/F, SVC для IM в тяжёлом режиме)\n100% / 2.5 Гц (V/F, SVC для PM в тяжёлом режиме)'
        S25 = 25, '100% / 0.5 Гц (V/F); 150% / 0.5 Гц (SVC)'
        S26 = 26, '150% / 3(1) Гц (V/F); 150% / 0.5 Гц (SVC)'
        S27 = 27, 'G type: 150% / 0.5 Гц; \nP type: 100% / 0.5 Гц'
        S28 = 28, 'Auto torque boost, manual torque boost 0.1%-30%; Vector torque boost 100-150; ' \
                  'Start frequency 0.4Hz-20Hz'
        S29 = 29, '150% / 0.5 Гц (SVC)'
        S30 = 30, 'G type: 150% / 0.5 Гц (SVC), 180% / 0 Гц (VC);\nP type: 100% / 0.5 Гц'
        S31 = 31, 'Auto torque boost, manual torque boost 0.1%-30%; ' \
                  'Cut-off frequency of torque boost 0Hz to maximum output frequency'
        S32 = 32, 'До 180% от номинального (Функция намагничивания постоянным током)'

    starting_torque = models.PositiveSmallIntegerField(
        verbose_name='Пусковой момент',
        choices=StartingTorque.choices,
        blank=True,
        null=True,
        help_text='Пусковой момент двигателя'
    )

    class CarrierFrequency(models.IntegerChoices):
        """Несущая частота ШИМ"""
        S20 = 20, '2...12 (Default: 3)'
        S21 = 21, '2...15'
        S22 = 22, '2...15 (Default: 4)'
        S23 = 23, '2...16 (Default: 4/3)'
        S24 = 24, '1...16/10/5 (Default: 6/4.5/3/1.8)'
        S25 = 25, '0.5...16'
        S26 = 26, '4...16 (Default: 4)'
        S27 = 27, '1...16'
        S30 = 30, '2...15/10/9 (Default: 8/6/4)'
        S31 = 31, '1...14 (Default: 8)'
        S32 = 32, '1...15 (Default: 8/4/2)'

    carrier_frequency = models.PositiveSmallIntegerField(
        verbose_name='Несущая частота ШИМ, кГц',
        choices=CarrierFrequency.choices,
        blank=True,
        null=True,
        help_text='Частота переключения силовых ключей'
    )

    class MultiPump(models.IntegerChoices):
        """Многонасосный режим"""
        W0 = 0, 'Нет'
        W10 = 10, 'Да, 2 насоса'
        W20 = 20, 'Да, до 3 насосов'
        W30 = 30, 'Да, до 4 насосов'
        W40 = 40, 'Да, до 8 насосов'

    multi_pump_system = models.PositiveSmallIntegerField(
        verbose_name='Много-насосный режим',
        choices=MultiPump.choices,
        blank=True,
        null=True,
        help_text='Поддержка управления несколькими насосами'
    )

    class DifferentEngines(models.IntegerChoices):
        """Работа с разными двигателями"""
        D0 = 0, 'Нет'
        D20 = 20, '2 группы параметров двигателей'
        D40 = 40, 'До 4 независимых групп параметров двигателя'

    different_engines_work = models.PositiveSmallIntegerField(
        verbose_name='Работа с разными двигателями',
        choices=DifferentEngines.choices,
        blank=True,
        null=True,
        help_text='Возможность работы с различными типами двигателей'
    )

    fire_mode = models.BooleanField(
        verbose_name='Пожарный режим',
        blank=True,
        null=True,
        help_text='Специальный режим для пожарных систем'
    )

    sleep_mode = models.BooleanField(
        verbose_name='Спящий режим',
        blank=True,
        null=True,
        help_text='Режим экономии энергии при простое'
    )

    flying_start = models.BooleanField(
        verbose_name='Подхват на ходу',
        blank=True,
        null=True,
        help_text='Возможность плавного подключения к вращающемуся двигателю'
    )

    class SkipFrequency(models.IntegerChoices):
        """Пропуск критических частот"""
        F0 = 0, 'Нет'
        F1 = 10, 'Пропуск одной полосы частот'
        F2 = 20, 'Пропуск 2-х полос частот'
        F3 = 30, 'Пропуск 3-х полос частот'
        F4 = 40, 'Пропуск 4-х полос частот'

    skip_frequency = models.PositiveSmallIntegerField(
        verbose_name='Пропуск критических частот',
        choices=SkipFrequency.choices,
        blank=True,
        null=True,
        help_text='Возможность исключения резонансных частот'
    )

    automatic_energy_saving = models.BooleanField(
        verbose_name='Автоматическое энергосбережение',
        blank=True,
        null=True,
        help_text='Автоматическая оптимизация энергопотребления'
    )

    class CoolingFanControl(models.IntegerChoices):
        """Управление вентилятором охлаждения"""
        F0 = 0, 'Нет'
        F10 = 10, 'Работает всё время при включении питания / при команде пуск'
        F20 = 20, 'Режим автоматического управления / работает всё время при включении питания'
        F30 = 30, 'Три режима работы, в том числе по температуре'
        F50 = 50, 'На выбор 5 режимов работы вентилятора'
        F51 = 51, 'На выбор 4 режима работы вентилятора'

    cooling_fan_control = models.PositiveSmallIntegerField(
        verbose_name='Управление вентилятором охлаждения',
        choices=CoolingFanControl.choices,
        blank=True,
        null=True,
        help_text='Режимы работы системы охлаждения'
    )

    class EngineProtection(models.IntegerChoices):
        """Защита двигателя"""
        P1 = 1, 'Перегрузка по току, перенапряжение, перегрев, потеря фазы и др.'

    engine_protection = models.PositiveSmallIntegerField(
        verbose_name='Защита двигателя',
        choices=EngineProtection.choices,
        blank=True,
        null=True,
        help_text='Встроенные функции защиты двигателя'
    )

    class StopPrevention(models.IntegerChoices):
        """Предотвращение перегрузки"""
        P10 = 10, 'Токоограничение при разгоне, замедлении и работе (общая настройка)'
        P11 = 11, 'Токоограничение при работе (общая настройка)'
        P20 = 20, 'Токоограничение при разгоне, замедлении и работе (независимые настройки)'
        P21 = 21, 'Токоограничение при разгоне, работе (независимые настройки)'

    stop_prevention = models.PositiveSmallIntegerField(
        verbose_name='Предотвращение перегрузки',
        choices=StopPrevention.choices,
        blank=True,
        null=True,
        help_text='Система предотвращения остановки при перегрузке'
    )

    automatic_start_after_power_loss = models.BooleanField(
        verbose_name='Преодоление провалов напряжения питания',
        blank=True,
        null=True,
        help_text='Автоматический перезапуск после восстановления питания'
    )

    class InputsOutputs(models.IntegerChoices):
        """Входы и выходы"""
        I10 = 10, 'DI: 4; AI: 1; TO: 0; RO: 1; AO: 1'
        I20 = 20, 'DI: 4; AI: 2; TO: 0; RO: 1; AO: 1'
        I30 = 30, 'DI: 5; AI: 1; TO: 1; RO: 1; AO: 1'
        I40 = 40, 'DI: 6; AI: 2; TO: 0; RO: 1; AO: 1'
        I41 = 41, 'DI: 5; AI: 2; TO: 1; RO: 1; AO: 1'
        I50 = 50, 'DI: 5; AI: 2; TO: 1; RO: 2; AO: 2'
        I60 = 60, 'DI: 6; AI: 2; TO: 1; RO: 2; AO: 2'
        I61 = 61, 'DI: 6; AI: 2; TO: 2; RO: 1; AO: 2'
        I70 = 70, 'DI: 7; AI: 2; TO: 3; RO: 1; AO: 1'
        I71 = 71, 'DI: 7; AI: 2; TO: 2; RO: 2; AO: 1'
        I72 = 72, 'DI: 8; AI: 2; TO: 2; RO: 1; AO: 1'
        I80 = 80, 'DI: 7; AI: 3; TO: 2; RO: 1; AO: 2'
        I81 = 81, 'DI: 8; AI: 2; TO: 2; RO: 2; AO: 2'
        I90 = 90, 'DI: 10; AI: 3; TO: 0; RO: 3; AO: 2'

    inputs_outputs = models.PositiveSmallIntegerField(
        verbose_name='Входы/выходы',
        choices=InputsOutputs.choices,
        blank=True,
        null=True,
        help_text='Количество дискретных/аналоговых входов и выходов'
    )

    io_expansion_boards = models.BooleanField(
        verbose_name='Платы расширения входов-выходов',
        blank=True,
        null=True,
        help_text='Возможность расширения количества I/O'
    )

    class PulseFrequencySetting(models.IntegerChoices):
        """Импульсное задание частоты"""
        IO0 = 0, 'Нет'
        IO1 = 1, 'Плата расширения'
        IO2 = 2, 'Да'

    pulse_frequency_setting = models.PositiveSmallIntegerField(
        verbose_name='Импульсное задание частоты',
        choices=PulseFrequencySetting.choices,
        blank=True,
        null=True,
        help_text='Возможность задания частоты импульсным сигналом'
    )

    class ControlPanel(models.IntegerChoices):
        """Панель управления"""
        P10 = 10, 'LED 4x7'
        P20 = 20, 'LED 5x7'
        P30 = 30, 'LED двухстрочный'
        P31 = 31, 'LED 5x7 (LCD опционально)'
        P32 = 32, 'LED двухстрочный (LCD опционально)'
        P60 = 60, 'LCD дисплей'
        P61 = 61, 'LCD базовая (LCD интеллектуальная опционально)'

    control_panel = models.PositiveSmallIntegerField(
        verbose_name='Панель управления',
        choices=ControlPanel.choices,
        blank=True,
        null=True,
        help_text='Тип дисплея и панели управления'
    )

    class Potentiometer(models.IntegerChoices):
        """Потенциометр"""
        P0 = 0, 'Нет'
        P10 = 10, 'Дополнительная плата потенциометра'
        P20 = 20, 'Потенциометр в панели управления'
        P30 = 30, 'Нажимное колёсико-энкодер'

    potentiometer = models.PositiveSmallIntegerField(
        verbose_name='Потенциометр',
        choices=Potentiometer.choices,
        blank=True,
        null=True,
        help_text='Наличие и тип потенциометра для ручного управления'
    )

    control_panel_included = models.BooleanField(
        verbose_name='Панель управления в комплекте',
        blank=True,
        null=True,
        help_text='Входит ли панель в базовую комплектацию'
    )

    class RemovablePanel(models.IntegerChoices):
        """Съёмная панель"""
        P0 = 0, 'Нет'
        P10 = 10, 'Для моделей от 22 кВт'
        P20 = 20, 'Да'

    removable_control_panel = models.PositiveSmallIntegerField(
        verbose_name='Съёмная панель',
        choices=RemovablePanel.choices,
        blank=True,
        null=True,
        help_text='Возможность снятия панели управления'
    )

    class PanelAtDistance(models.IntegerChoices):
        """Выносная панель"""
        P0 = 0, 'Нет'
        P10 = 10, 'Да, при помощи кабеля-аксессуара'
        P11 = 11, 'Да'
        P12 = 12, 'Да, разъем ВН-10 (IDC-10MS)'
        P20 = 20, 'Да, соединение обычным патч-кордом'

    control_panel_at_distance = models.PositiveSmallIntegerField(
        verbose_name='Выносная панель',
        choices=PanelAtDistance.choices,
        blank=True,
        null=True,
        help_text='Возможность дистанционного размещения панели'
    )

    class Configurations(models.IntegerChoices):
        """Предварительные конфигурации"""
        C0 = 0, 'Нет'
        C10 = 10, 'Группировка параметров по применениям'
        C11 = 11, 'Макросы по применениям'
        C12 = 12, 'Группировка параметров пользователя'
        C20 = 20, 'Макросы, мастера настроек'

    pre_configurations = models.PositiveSmallIntegerField(
        verbose_name='Предварительные конфигурации (Макросы)',
        choices=Configurations.choices,
        blank=True,
        null=True,
        help_text='Встроенные шаблоны настроек для типовых применений'
    )

    class BackupSettings(models.IntegerChoices):
        """Копирование/бэкап настроек"""
        S0 = 0, 'Нет'
        S20 = 20, 'Да (LCD панель)'
        S21 = 21, 'Да (только для дистанционного управления)'
        S40 = 40, 'Да'

    copy_backup_settings = models.PositiveSmallIntegerField(
        verbose_name='Копирование/бэкап настроек',
        choices=BackupSettings.choices,
        blank=True,
        null=True,
        help_text='Возможность сохранения и восстановления параметров'
    )

    pid_controller = models.IntegerField(
        verbose_name='Встроенный ПИД-регулятор',
        blank=True,
        null=True,
        help_text='Количество встроенных ПИД-контуров'
    )

    class Communications(models.IntegerChoices):
        """Протоколы связи"""
        C0 = 0, 'Нет'
        C10 = 10, 'Плата расширения: Modbus RTU'
        C20 = 20, 'Платы расширения: Modbus RTU, Profibus DP'
        C30 = 30, 'Встроен: Modbus RTU'
        C40 = 40, 'Встроен: Modbus RTU; Платы расширения: Profibus DP'
        C41 = 41, 'Платы расширения: Modbus RTU, Ethernet, Profibus DP, ProfiNet IO, DeviceNet, CANopen, EtherCAT'
        C50 = 50, 'Встроен: Modbus RTU; Платы расширения: Ethernet, Profibus DP'
        C60 = 60, 'Встроен: Modbus RTU; Платы расширения: Profibus DP, CANopen, CANlink'
        C70 = 70, 'Встроен: Modbus RTU; Платы расширения: Ethernet, DeviceNet, CANopen, Profibus DP'
        C80 = 80, 'Встроены: Modbus RTU, BACnet; Платы расширения: Ethernet, DeviceNet, CANopen, Profibus DP'

    communications = models.PositiveSmallIntegerField(
        verbose_name='Протоколы связи',
        choices=Communications.choices,
        blank=True,
        null=True,
        help_text='Поддерживаемые интерфейсы и протоколы связи'
    )

    class Plc(models.IntegerChoices):
        """Встроенный ПЛК"""
        PO = 0, 'Нет'
        P2 = 2, 'ПЛК на 2000 шагов'
        P3 = 3, 'ПЛК на 10000 шагов'

    built_in_plc = models.PositiveSmallIntegerField(
        verbose_name='Встроенный ПЛК',
        choices=Plc.choices,
        blank=True,
        null=True,
        help_text='Встроенный программируемый логический контроллер'
    )

    class Encoder(models.IntegerChoices):
        """Подключение энкодера"""
        PO = 0, 'Нет'
        P10 = 10, 'Импульсный вход (плата расширения)'
        P20 = 20, 'Импульсный вход'
        P50 = 50, 'Плата расширения энкодера (ABZ, UVW, Rotary transformer)'
        P51 = 51, 'Плата расширения энкодера'

    encoder_support = models.PositiveSmallIntegerField(
        verbose_name='Подключение энкодера',
        choices=Encoder.choices,
        blank=True,
        null=True,
        help_text='Возможность подключения энкодера для обратной связи'
    )

    sto_function = models.BooleanField(
        verbose_name='Стандарт безопасности STO',
        blank=True,
        null=True,
        help_text='Функция безопасного отключения крутящего момента'
    )

    class ExternalPower(models.IntegerChoices):
        """Подключение резервного питания +24В"""
        P0 = 0, 'Нет'
        P1 = 1, 'Опциональная плата'
        P2 = 2, 'Да'

    external_power_24v = models.PositiveSmallIntegerField(
        verbose_name='Подключение резервного питания +24В',
        choices=ExternalPower.choices,
        blank=True,
        null=True,
        help_text='Возможность подключения внешнего питания 24В'
    )

    class Usb(models.IntegerChoices):
        """Встроенный порт USB"""
        U0 = 0, 'Нет'
        U1 = 1, 'Есть (загрузка и выгрузка даже без включения питания)'

    built_in_usb = models.PositiveSmallIntegerField(
        verbose_name='Встроенный порт USB',
        choices=Usb.choices,
        blank=True,
        null=True,
        help_text='Наличие USB порта для программирования'
    )

    class PCSoft(models.IntegerChoices):
        """Софт для отладки на ПК"""
        S0 = 0, 'Нет'
        S30 = 30, 'Да'

    pc_soft = models.PositiveSmallIntegerField(
        verbose_name='Софт для отладки на ПК',
        choices=PCSoft.choices,
        blank=True,
        null=True,
        help_text='Программное обеспечение для настройки с компьютера'
    )

    class EmcFilter(models.IntegerChoices):
        """Встроенный EMC фильтр"""
        E0 = 0, 'Нет'
        E10 = 10, '1x230В: C3; 3x400В: контур ЭМС-фильтра'
        E11 = 11, 'Контур ЭМС-фильтра'
        E20 = 20, 'C3 (для эксплуатации в промышленной зоне)'
        E30 = 30, 'C2 (для эксплуатации в жилой зоне)'

    emc_filter = models.PositiveSmallIntegerField(
        verbose_name='Встроенный EMC фильтр',
        choices=EmcFilter.choices,
        blank=True,
        null=True,
        help_text='Встроенный фильтр электромагнитной совместимости'
    )

    class ChokeDc(models.IntegerChoices):
        """Дроссель в звене постоянного тока"""
        C0 = 0, 'Нет'
        C10 = 10, 'Опция от 75кВт'
        C20 = 20, 'Опция 45...400кВт, встроен от 450кВт'
        C30 = 30, 'Опция'
        C40 = 40, 'Встроен на мощности 11, 15 кВт и от 200 кВт'
        C50 = 50, 'Встроен на мощности от 45 кВт'
        C60 = 60, 'Встроен на мощности от 37 кВт'
        C70 = 70, 'Встроен'

    choke_dc_link = models.PositiveSmallIntegerField(
        verbose_name='Дроссель в звене постоянного тока',
        choices=ChokeDc.choices,
        blank=True,
        null=True,
        help_text='Встроенный дроссель для сглаживания тока'
    )

    class BrakeInterrupter(models.IntegerChoices):
        """Тормозной прерыватель"""
        C0 = 0, 'Нет'
        C10 = 10, 'Встроен на мощности до 15 кВт'
        C20 = 20, 'Встроен на мощности до 22 кВт'
        C30 = 30, 'Встроен на мощности до 30 кВт'
        C40 = 40, 'Встроен на мощности до 37 кВт'
        C50 = 50, 'Встроен на мощности до 45 кВт'
        C60 = 60, 'Встроен'

    brake_interrupter = models.PositiveSmallIntegerField(
        verbose_name='Тормозной прерыватель',
        choices=BrakeInterrupter.choices,
        blank=True,
        null=True,
        help_text='Встроенный тормозной прерыватель для рекуперации энергии'
    )

    class MotorCable(models.IntegerChoices):
        """Максимальная длина кабеля двигателя"""
        D10 = 10, 'Без дросселя: до 50м; С дросселем: до 100м'
        D11 = 11, 'Если длина кабелей двигателя превышает 50 м, рекомендуется использовать моторный дроссель.'
        D12 = 12, 'Без дросселя: до 50м; С дросселем: до 100м; EMC C3: до 30м'
        D20 = 20, 'Если длина кабелей двигателя превышает 100 м, рекомендуется использовать моторный дроссель.'
        D30 = 30, 'Без дросселя: экран.кабель 35...100м в зависимости от номинала; неэкран. 50...150м. \n' \
                  'С дросселем: экран.кабель 50...150м; неэкран. 90...225м'
        D40 = 40, 'Без дросселя: экран.кабель 50...150м в зависимости от номинала; неэкран. 75...225м. \n' \
                  'С дросселем: экран.кабель 75...225м; неэкран. 115...325м'

    motor_cable_length = models.PositiveSmallIntegerField(
        verbose_name='Максимальная длина кабеля двигателя',
        choices=MotorCable.choices,
        blank=True,
        null=True,
        help_text='Допустимая длина соединительного кабеля с двигателем'
    )

    quick_change_fans = models.BooleanField(
        verbose_name='Быстросъёмные вентиляторы',
        blank=True,
        null=True,
        help_text='Возможность быстрой замены вентиляторов охлаждения'
    )

    dual_circuit_cooling = models.BooleanField(
        verbose_name='Двухконтурное охлаждение',
        blank=True,
        null=True,
        help_text='Раздельное охлаждение силовых и управляющих цепей'
    )

    class OperatingTemp(models.IntegerChoices):
        """Рабочая температура"""
        T10 = 10, '-10...+40'
        T20 = 20, '-10...+40; \nСо снижением характеристик -10...+50'
        T21 = 21, '-10...+40(50)'
        T30 = 30, '-10...+40(50); \nСо снижением характеристик -10...+60'
        T40 = 40, '-10...+50; \nСо снижением характеристик -10...+60'
        T50 = 50, '-20...+50; \nСо снижением характеристик -20...+60'

    operating_temp = models.PositiveSmallIntegerField(
        verbose_name='Рабочая температура, ℃',
        choices=OperatingTemp.choices,
        blank=True,
        null=True,
        help_text='Диапазон рабочих температур окружающей среды'
    )

    class Humidity(models.IntegerChoices):
        """Относительная влажность"""
        H20 = 20, 'Макс. 60%'
        H40 = 40, 'Макс. 90%'
        H50 = 50, 'Макс. 95%'

    use_relative_humidity = models.PositiveSmallIntegerField(
        verbose_name='Относительная влажность при эксплуатации',
        choices=Humidity.choices,
        blank=True,
        null=True,
        help_text='Максимальная допустимая влажность воздуха'
    )

    class Altitude(models.IntegerChoices):
        """Высота установки"""
        A1 = 1, 'До 1000м'
        A2 = 2, 'До 1000м; Свыше 1000м со снижением характеристик'

    installation_altitude = models.PositiveSmallIntegerField(
        verbose_name='Высота установки',
        choices=Altitude.choices,
        blank=True,
        null=True,
        help_text='Допустимая высота установки над уровнем моря'
    )

    class WallToWall(models.IntegerChoices):
        """Монтаж "Стенка к стенке"""
        W0 = 0, 'Нет'
        W10 = 10, 'Допускается для ПЧ от 45 кВт включительно; \nДо 45 кВт: зазор 10мм'
        W20 = 20, 'Допускается при -20...+40℃, \nдо +50℃ со снижением характеристик'
        W21 = 21, 'Допускается при -20...+40℃'
        W30 = 30, 'Допускается'

    wall_to_wall_installation = models.PositiveSmallIntegerField(
        verbose_name='Монтаж "Стенка к стенке"',
        choices=WallToWall.choices,
        blank=True,
        null=True,
        help_text='Возможность установки без зазоров между корпусами'
    )

    class RailwayMounting(models.IntegerChoices):
        """Монтаж на дин-рейку"""
        R0 = 0, 'Нет'
        R10 = 10, 'Монтажный комплект на DIN-рейку'
        R20 = 20, 'Да'

    railway_mounting = models.PositiveSmallIntegerField(
        verbose_name='Монтаж на дин-рейку',
        choices=RailwayMounting.choices,
        blank=True,
        null=True,
        help_text='Возможность крепления на DIN-рейку'
    )

    class ProtectionDegree(models.IntegerChoices):
        """Степень защиты"""
        D1 = 1, 'IP20'
        D2 = 2, 'IP21'
        D3 = 3, 'IP55'

    protection_degree = models.PositiveSmallIntegerField(
        verbose_name='Степень защиты',
        choices=ProtectionDegree.choices,
        blank=True,
        null=True,
        help_text='Класс защиты корпуса от пыли и влаги'
    )

    class BoardsProtection(models.IntegerChoices):
        """Защита печатных плат"""
        P0 = 0, 'Нет'
        P10 = 10, 'Специальное покрытие печатных плат'
        P11 = 11, 'Трёхслойное защитное покрытие'

    circuit_boards_protection = models.PositiveSmallIntegerField(
        verbose_name='Защита печатных плат',
        choices=BoardsProtection.choices,
        blank=True,
        null=True,
        help_text='Дополнительная защита электронных компонентов'
    )

    class MinimumSize(models.IntegerChoices):
        """Минимальный габарит"""
        P31 = 31, '186x125x170'  # HV610
        P32 = 32, '175x105x161'  # EM60
        P33 = 33, '167x109x161'  # EM100/102
        P34 = 34, '180x130x148'  # EM180
        P35 = 35, '190x104x148'  # RI9000
        P40 = 40, '202x70x161'   # ACS355
        P41 = 41, '212x95x154'   # HV100
        P42 = 42, '142x72x159'   # MS300
        P43 = 43, '159x96x133'   # Canroon VFC300
        P50 = 50, '170x78x134'   # HV10
        P51 = 51, '142x72x143'   # ME300
        P52 = 52, '176x90x145'   # HV480
        P53 = 53, '184x85x145'   # D200
        P54 = 54, '184x98x135'   # RI3000

    minimum_size = models.PositiveSmallIntegerField(
        verbose_name='Минимальный габарит, ВхШхГ',
        choices=MinimumSize.choices,
        blank=True,
        null=True,
        help_text='Габаритные размеры корпуса в мм'
    )

    class PackageSet(models.IntegerChoices):
        """Комплект поставки, упаковка"""
        P0 = 0, 'Нет'
        P20 = 20, 'Плотный картон, вспененный полиэтилен, сокращённый мануал'
        P21 = 21, 'Плотный картон, вспененный полиэтилен, полный мануал'
        P22 = 22, 'Плотный картон, краткая инструкция по вводу в эксплуатацию'
        P23 = 23, 'Простая упаковка: картон, две вставки из вспененного полиэтилена, пакет, силикагель. ' \
                  'Полный мануал на русском языке.'
        P30 = 30, 'Простая упаковка: картон, две вставки из вспененного полиэтилена, пакет, силикагель. ' \
                  'Информативная этикетка (модель, мощность, сеть, выходные параметры. Сокращённый мануал. ' \
                  'Монтажный комплект пульта на дверь (постель, кабель 1.5м). Резиновые сальники (3шт)'
        P40 = 40, 'Плотный картон, надувная пузырчатая пленка, сокращённый мануал'
        P41 = 41, 'Плотный картон, надувная пузырчатая пленка, полный мануал'
        P42 = 42, 'Плотный картон, сокращённый мануал'
        P43 = 43, 'Плотный картон, надувная пузырчатая пленка, сокращённый мануал, отвертка для цепей управления'
        P50 = 50, 'Плотный картон, надувная пузырчатая пленка, полный мануал на русском языке.'

    package_set = models.PositiveSmallIntegerField(
        verbose_name='Комплект поставки, упаковка',
        choices=PackageSet.choices,
        blank=True,
        null=True,
        help_text='Качество упаковки и комплектность поставки'
    )

    class CaseQuality(models.IntegerChoices):
        """Качество корпуса"""
        P10 = 10, 'Прочный корпус; неудобное снятие клеммной крышки, дребезжит крышка вентилятора'
        P11 = 11, 'Прочный корпус. Плавные скругленные линии. При нажатии на кнопки на панели корпус скрипит немного'
        P12 = 12, 'Прочный пластик, есть некритичный запах. Шумная работа кулера и дребезг.'
        P20 = 20, 'Прочный пластик, есть некритичный запах'
        P30 = 30, 'Прочный корпус, качественная сборка; чёрный матовый, не вонючий пластик'
        P31 = 31, 'Прочный корпус, качественная сборка'

    case_quality = models.PositiveSmallIntegerField(
        verbose_name='Качество корпуса',
        choices=CaseQuality.choices,
        blank=True,
        null=True,
        help_text='Оценка качества изготовления корпуса'
    )

    description = models.TextField('Описание', blank=True, help_text='Подробное описание серии и её особенностей')

    def __str__(self) -> str:
        return str(f'{self.brand} {self.name}')

    class Meta:
        verbose_name = 'Серия'
        verbose_name_plural = 'Серии'
        ordering = ('brand', 'name')


class FrequencyDrive(models.Model):
    """
    Конкретные модели частотных преобразователей.

    Отдельные VFD с конкретными техническими параметрами:
    мощность, напряжение, ток в рамках определенной серии.
    """
    article = models.CharField('Артикул', max_length=30, unique=True, help_text='Уникальный артикул модели')
    name = models.CharField('Наименование', max_length=200, blank=True,
                            null=True, help_text='Полное наименование модели')
    series = models.ForeignKey(Series, verbose_name='Серия', on_delete=models.PROTECT,
                               help_text='Серия, к которой относится модель')
    power = models.FloatField('Мощность', help_text='Номинальная мощность в кВт')
    current = models.FloatField('Ток', blank=True, null=True, help_text='Номинальный выходной ток в А')

    VOLT_CHOICES = (
        (400, 400),
        (230, 230),
    )
    voltage = models.FloatField('Напряжение', default=380, choices=VOLT_CHOICES, help_text='Входное напряжение в В')

    def __str__(self) -> str:
        return str(f'{self.article}')

    class Meta:
        verbose_name = 'Частотник'
        verbose_name_plural = 'Частотники'
        ordering = ('series__brand', 'series__name', 'voltage', 'power')


class AccessoryType(models.Model):
    """
    Типы аксессуаров для частотных преобразователей.

    Фильтры, дроссели, панели управления и другое дополнительное оборудование.
    """
    name = models.CharField('Наименование', max_length=200, unique=True, help_text='Тип аксессуара')

    def __str__(self) -> str:
        return str(self.name)

    class Meta:
        verbose_name = 'Тип аксессуара'
        verbose_name_plural = 'Типы аксессуаров'


class Accessory(models.Model):
    """
    Аксессуары для частотных преобразователей.

    Дополнительное оборудование, совместимое с определенными сериями VFD.
    """
    article = models.CharField('Артикул', max_length=30, unique=True, help_text='Уникальный артикул аксессуара')
    name = models.CharField('Наименование', max_length=200, blank=True,
                            null=True, help_text='Полное наименование аксессуара')
    type = models.ForeignKey(AccessoryType, verbose_name='Тип аксессуара',
                             on_delete=models.PROTECT, help_text='Тип аксессуара')
    series = models.ManyToManyField(Series, verbose_name='Серии', help_text='Серии VFD, с которыми совместим аксессуар')

    def __str__(self) -> str:
        return str(f'{self.article}')

    class Meta:
        verbose_name = 'Аксессуар'
        verbose_name_plural = 'Аксессуары'
        ordering = ('type', 'article')


class Price(models.Model):
    """
    Цены на оборудование от различных поставщиков.

    Связывает товары (VFD или аксессуары) с поставщиками и их ценами
    для сравнения предложений.
    """
    frequency_drive = models.ForeignKey(
        FrequencyDrive,
        verbose_name='Частотник',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        help_text='Частотный преобразователь (заполняется для VFD)'
    )
    accessory = models.ForeignKey(
        Accessory,
        verbose_name='Аксессуар',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        help_text='Аксессуар (заполняется для дополнительного оборудования)'
    )
    supplier = models.ForeignKey(Supplier, verbose_name='Поставщик', on_delete=models.PROTECT,
                                 help_text='Поставщик, предлагающий товар')
    price = models.FloatField('Цена', help_text='Цена в валюте поставщика')

    def __str__(self) -> str:
        return str(f'{self.price}')

    class Meta:
        verbose_name = 'Цена'
        verbose_name_plural = 'Цены'
