import os
import shutil
import click

ROOT_PATH = "./root/"
EXTRA_PATH ="./root/extra/"
PAYLOAD_PATH = "./root/payload/"
#                          #
# Shell complete functions #
#                          #
def complete_payloads(ctx, param, incomplete):
    payloads = getAllPayloads()
    return [
        payload for payload in payloads if payload.startswith(incomplete)
    ]

def complete_categories(ctx, param, incomplete):
    categories = getChildDirectories(EXTRA_PATH)
    return [
       category for category in categories if category.startswith(incomplete)
    ]

#                        #
# Payload data functions #
#                        #
def getAllPayloads():
    categories = getChildDirectories(EXTRA_PATH)
    payloads = []
    for category in categories:
        categoryPayloads = getChildDirectories(EXTRA_PATH + category)
        for categoryPayload in categoryPayloads:
            payloads = payloads + [f'{category}_{categoryPayload}']
    print(payloads)
    return payloads

def getPayloadsForCategories(categories):
    payloads = {}
    for category in categories:
            payloads[category] = getChildDirectories(EXTRA_PATH + category)
    return payloads

def getCurrentPayload():
    currentPayloadFile = open(f'{PAYLOAD_PATH}currentpayload.txt', "r+")
    currentPayload = currentPayloadFile.read()
    currentPayloadFile.close()
    return currentPayload


#                #
# File functions #
#                #


def getChildDirectories(parent):
    return next(os.walk(parent))[1]


def getFilesToMove(srcDir):
    return os.listdir(srcDir)

def deleteOldFiles():
    click.echo('Removing previous payload files')
    shutil.rmtree(PAYLOAD_PATH)

def copyPayloadFilesToPayloadDir(payloadDir, payloadFiles):
    click.echo('Moving the follwing files: ' + ', '.join(payloadFiles))
    shutil.copytree(payloadDir, PAYLOAD_PATH)

def setCurrentPayload(category,payload):
    click.echo('Setting the current payload')
    currentPayloadFile = open(f'{PAYLOAD_PATH}currentpayload.txt', "a+")
    currentPayloadFile.write(f'{category}_{payload}')
    currentPayloadFile.close()

def copyPayloadWithSCP(sshAddress, payloadDir):
    os.system(f'scp {payloadDir}/* {sshAddress}:/root/payload/')


#                 #
# Print functions #
#                 #

def printCategories(categories):
    click.echo(click.style('Categories:', bold=True))
    for category in categories:
        click.echo(category)


def printPayloads(payloads):
    for category in payloads:
        click.echo(click.style(f'{category} payloads', bold=True))
        for payload in payloads[category]:
            click.echo(payload)
        click.echo('')

# # # # # # # # # # #
#                   #
# COMMAND: SHARKPM  #
#                   #
# # # # # # # # # # #

@click.group()
def sharkpm():
    pass

# # # # # # # # #
#               #
# COMMAND: LIST #
#               #
# # # # # # # # #

@click.command()
@click.option('-c', '--category', default='', help='Specify a category of payload to list', required=False, shell_complete=complete_categories)
@click.option('-s', '--show-payloads', default=False, help='If Present, Will list payloads', is_flag=True)
def list(category, show_payloads):
    categories = getChildDirectories(EXTRA_PATH)
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


# # # # # # # # #
#               #
#  COMMAND: GET #
#               #
# # # # # # # # #

@click.command()
def get():
    full = getCurrentPayload().split('_')
    category = full[0]
    payload = full[1]
    click.echo(f'Current payload category: {click.style(category, bold=True)}')
    click.echo(f'Current payload: {click.style(payload, bold=True)}')


# # # # # # # # #
#               #
# COMMAND: SET  #
#               #
# # # # # # # # #

@click.command()
@click.option('-p', '--payload', default='', help='Specify the payload in the format {category}_{payload}', required=False, shell_complete=complete_payloads)
@click.option('-s', '--ssh-address', default='', help='User and Host to copy files to', required=False)
def set(payload, ssh_address):
    categoryOptions = getChildDirectories(EXTRA_PATH)
    category = ''
    if payload == '' :
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
    else:
        category = payload.split('_')[0]
        payload = payload.split('_')[1]

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

    payloadDir = EXTRA_PATH + category + '/' + payload

    payloadFiles = getFilesToMove(payloadDir)
    if ssh_address == '':
        deleteOldFiles()
        copyPayloadFilesToPayloadDir(payloadDir, payloadFiles)
        setCurrentPayload(category, payload)
    else:
        copyPayloadWithSCP(ssh_address, payloadDir)
    click.echo(click.style(payload + ' is now active', bold=True))


sharkpm.add_command(list)
sharkpm.add_command(set)
sharkpm.add_command(get)


if __name__ == '__main__':
    sharkpm()
