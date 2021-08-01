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
@click.option('-c', '--category', default='', help='Specify a category of payload to list', required=False)
@click.option('-s', '--show-payloads', default=False, help='If Present, Will list payloads', is_flag=True)
def list(category, show_payloads):
    categories = getChildDirectories('extra')
    payloads = {}

    if show_payloads == True:
        click.echo(click.style('Showing Payloads', italic=True))
        payloads = getPayloadsForCategories(categories)
        printPayloads(payloads)
        return

    if category != '' and category in categories:
        payloads = getPayloadsForCategories([category])
        printPayloads(payloads)
        return

    printCategories(categories)



def getPayloadsForCategories(categories):
    payloads = {}
    for cat in categories:
            payloads[cat] = getChildDirectories('extra/' + cat)
    return payloads

def printCategories(categories):
    click.echo(click.style('Categories:', bold=True))
    for cat in categories:
        click.echo(cat)

def getChildDirectories(parent):
    return next(os.walk(parent))[1]


def printPayloads(payloads):
    for category in payloads:
        click.echo(click.style(f'{category} payloads', bold=True))
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
    full = getCurrentPayload().split(':')
    category = full[0]
    payload = full[1]
    click.echo(f'Current payload category: {click.style(category, bold=True)}')
    click.echo(f'Current payload: {click.style(payload, bold=True)}')


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
@click.option('-c', '--category', default='', help='Specify the payload category', required=False)
@click.option('-p', '--payload', default='', help='Specify the payload', required=False)
def set(category, payload):
    categoryOptions = getChildDirectories('extra')

    if category == '' :
        click.echo('No category provided')
        category = click.prompt(
            click.style(
                'Please Select A Category: ',
                bold=True
                ),
            default='',
            type=click.Choice(categoryOptions),
            show_default=True,
            show_choices=True
        )

    if category not in categoryOptions:
        click.echo('Invalid category')
        return

    payloadOptions = getPayloadsForCategories([category])

    if payload == '' :
        click.echo('No Payload Provided')
        payload = click.prompt(
            click.style(
                'Please Select A Payload: ',
                bold=True
                ),
            default='',
            type=click.Choice(payloadOptions[category]),
            show_default=True,
            show_choices=True
        )

    payloadDir = 'extra/' + category + '/' + payload

    payloadFiles = getFilesToMove(payloadDir)

    deleteOldFiles()
    copyPayloadFilesToPayloadDir(payloadDir, payloadFiles)
    setCurrentPayload(category, payload)
    click.echo(click.style(payload + ' is now active', bold=True))


def getFilesToMove(srcDir):
    return os.listdir(srcDir)

def deleteOldFiles():
    click.echo('Removing previous payload files')
    shutil.rmtree('payload')

def copyPayloadFilesToPayloadDir(payloadDir, payloadFiles):
    click.echo('Moving the follwing files: ' + ', '.join(payloadFiles))
    shutil.copytree(payloadDir, 'payload')

def setCurrentPayload(category,payload):
    click.echo('Setting the current payload')
    currentPayloadFile = open('payload/currentpayload.txt', "a+")
    currentPayloadFile.write(f'{category}:{payload}')
    currentPayloadFile.close()


cli.add_command(list)
cli.add_command(set)
cli.add_command(get)


if __name__ == '__main__':
    cli()
