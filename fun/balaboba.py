from aiobalaboba import Balaboba


async def bala(text):
    bb = Balaboba()

    # Get text types
    intros = await bb.intros(language="ru")

    # Get the first text type
    intro = next(intros)

    # Print Balaboba's response to the "Hello" query
    response = await bb.balaboba(text, intro=intro.number)
    return response

