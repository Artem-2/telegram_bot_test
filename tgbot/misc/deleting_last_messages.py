
async def deleting_last_messages(state):
    try:
        data = await state.get_data()
        last_message = data["last_message"]
        await last_message.delete()
        last_message = None
        await state.update_data(last_message=last_message)
    except:
        last_message = None
        await state.update_data(last_message=last_message)