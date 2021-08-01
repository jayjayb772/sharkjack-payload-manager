import os
import shutil
import click


@click.group()
def cli():
    pass

# # # # # # # # #
#               #
# COMMAND: LIST #
#               #
# # # # # # # # #

@click.command()
@click.option('--showpayloads', default=False, help='If true (t, true, True), will list payload in categories', required=False)
@click.option('--category', default='', help='Specify a category of payload to list', required=False)
def list(showpayloads, category):
    categories = getChildDirectories('extra')
    payloads = {}
    if showpayloads == 'true' or showpayloads == 't' or showpayloads == True:
        click.echo(click.style('Showing Payloads', italic=True))
        for cat in categories:
            payloads[cat] = getChildDirectories('extra/' + cat)
        printPayloads(payloads)
        return

    if category != '' and category in categories:
        payloads[category] = getChildDirectories('extra/' + category)
        printPayloads(payloads)
        return

    click.echo(click.style('Categories:', bold=True))
    for cat in categories:
        click.echo(cat)


def getChildDirectories(parent):
    return next(os.walk(parent))[1]


def printPayloads(payloads):
    for category in payloads:
        click.echo(click.style(category, bold=True))
        for payload in payloads[category]:
            click.echo(payload)
        click.echo('')

# # # # # # # # #
#               #
#  COMMAND: GET #
#               #
# # # # # # # # #
@click.command()
def get():
    click.echo(getCurrentPayload())

def getCurrentPayload():
    currentPayloadFile = open('payload/currentpayload.txt', "r+")
    currentPayload = currentPayloadFile.read()
    currentPayloadFile.close()
    return currentPayload



# # # # # # # # #
#               #
# COMMAND: SET  #
#               #
# # # # # # # # #
@click.command()
@click.option('--payload', default='', help='Name of the payload to switch to')
@click.option('--category', default='', help='Category of the payload to switch to')
@click.option('--whole', default='', help='Category and payload to switch to in \'category:payload\' Format')
def set(payload, category, whole):
    if whole == '' and (payload == '' or category == ''):
        click.echo(click.style('Invalid parameters', bold=True))
        click.echo('--payload and --category are required')
        click.echo('or')
        click.echo('--whole is required')
        return
    if whole != '':
        wholeSplit = whole.split(':')
        category = wholeSplit[0]
        payload = wholeSplit[1]

    payloadDir = 'extra/' + category + '/' + payload

    payloadFiles = getFilesToMove(payloadDir)

    deleteOldFiles()
    copyPayloadFilesToPayloadDir(payloadDir, payloadFiles)
    setCurrentPayload(payload)
    click.echo(click.style(payload + ' is now active', bold=True))


def getFilesToMove(srcDir):
    return os.listdir(srcDir)

def deleteOldFiles():
    click.echo('Removing previous payload files')
    shutil.rmtree('payload')


def copyPayloadFilesToPayloadDir(payloadDir, payloadFiles):
    click.echo('Moving the follwing files: ' + ', '.join(payloadFiles))
    shutil.copytree(payloadDir, 'payload')


def setCurrentPayload(payload):
    click.echo('Setting the current payload')
    currentPayloadFile = open('payload/currentpayload.txt', "a+")
    currentPayloadFile.write(payload)
    currentPayloadFile.close()


cli.add_command(list)
cli.add_command(set)
cli.add_command(get)


if __name__ == '__main__':
    cli()
