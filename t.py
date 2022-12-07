from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests

def ask(question,ids=None,isvariant=False):
	if ids and len(ids)==4:
		if isvariant:
			pdata={'question':question,'parent_message_id':ids[2],'_id':ids[3],'conversation_id':ids[0]}
		else:
			pdata={'question':question,'parent_message_id':ids[1],'_id':None,'conversation_id':ids[0]}
	else:
		pdata={'question':question,'parent_message_id':None,'_id':None,'conversation_id':None}
	r=requests.post('http://127.0.01:88/ask',data=pdata)
	return r.content.decode()


async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	mdic=update.message.to_dict()
	if 'reply_to_message' in mdic and 'conversation_id' in mdic['reply_to_message']['text']:
		ids=mdic['reply_to_message']['text'].split('conversation_id:')[-1].split('||\n')[0].split(',')
		question=mdic['reply_to_message']['text'].split('question:|')[-1].split('|conversation_id')[0]
		q2=' '.join(context.args)
		if len(q2)>0:
			question=q2
		answer=ask(question,ids,bool(len(context.args)==0))
	else:
		answer=ask(' '.join(context.args))
	await update.message.reply_text(answer)#, parse_mode='Markdown')

if __name__ == "__main__":
	app = ApplicationBuilder().token('<TELEGRAM BOT TOKEN>').build()
	app.add_handler(CommandHandler("ask", ask))
	app.run_polling()