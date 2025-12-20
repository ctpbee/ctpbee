import click
import os


@click.group()
def cli():
    pass


def exec_command(password, command):
    if password is None:
        pass
    else:
        command = "echo %s|sudo -S %s" % (password, command)
    click.echo(f"exec: {command}")
    os.system(command)


def append_text_to_locale(password, text):
    if password is not None:
        command = (
            f"echo {password} | sudo -S echo  {text} | sudo tee -a /etc/locale.gen"
        )
    else:
        command = f"echo {text} | tee -a /etc/locale.gen"
    click.echo(f"exec: {command}")
    os.system(command)


@click.command()
@click.option(
    "--password", default=None, help="当前用户密码, 用以执行更新locale.gen文件"
)
def init_locale(password):
    append_text_to_locale(password=password, text="zh_CN.GB18030 GB18030")
    append_text_to_locale(password=password, text="en_US.UTF-8 UTF-8")
    append_text_to_locale(password=password, text="zh_CN.UTF-8 UTF-8")
    exec_command(password=password, command="locale-gen")


cli.add_command(init_locale)
