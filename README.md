Config Validator
================

Project is not fully documented, but I'am working on it.
Please contact me at zverev.s.v[at]inbox.ru, if you have any questions.

This project serves for checking complex configuration files of any application
or system daemon written in python before it starts to serve. Just like running
apache web server with option '-t' (test config).

Configuration should be some complex data structure (or simple), for example a
dictionary with nested list ot dictionaries or scalar values. For example
configuration may be loaded from some 'yaml' file with the use of standard
python libraby package. Typical example of complex nested configuration
performed as dictionary is python's standard library's package 'logging'.

To use this in your project you need to import it at, provide the configuration
and a 'configuration schema'. Configuration schema is something like rules or
definitions for possible values of any inner node or leaf of your configuration.

See example.py to examine the simplicity of its usage.

Project includes configuration schema for python's standard library 'logging'.

Project is written in good OOP and is highly extendable. See "Extend HowTo" at
README.rst .

--------------------------------------------------------------------------------

Проект покрыт документацией не полностью, но я работаю над этим. Если у Вас
возникают вопросы, смело пишите мне на zverev.s.v[at]inbox.ru.

Этот проект - утилита для проверки сложной конфигурации какого-либо приложения
или системного демона написанных на языке python. Примерно как при запуске веб
сервера apache с ключем '-t' для проверки правильности конфигурации.

Под конфигурацией имеется в виду сложная структурированное значение (может быть
и простое), например словарь со вложенными списками или другими словарями или
более простыми значениями в качестве внутренних узлов или листьев дерева.
Типичным примером конфигурации реализованной в виде сложного словаря может быть
конфигурация для пакета из стандартной библиотеки питона 'logging'.

Чтобы воспользоваться валидатором конфигурации, Вам следует импортировать его
в своем проекте, подготовить конфигурацию и так называемую 'схему конфигурации'.
Схема конфигурации это некоторые правила или определения, которые описывают
возможные значения для внутреннего или краевого узла конфигурации.

Смотрите example.py чтобы убедиться в простоте использования валидатора.

В проекте уже есть схема для проверки конфигурации для пакета 'logging' из
стандартной библиотеки языка python.

Проект написан в хорошем ООП стиле и поэтому расширяем и гибок для доработок.
Смотрите секцию 'Extend HowTo' в файле README.rst с инструкциями по расширению
типов проверок или данных.

