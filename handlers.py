from sheets_client import append_lead
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

router = Router()

# Define FSM states for the customer survey
class OrderForm(StatesGroup):
    waiting_for_name = State()   # Waiting for user's name
    waiting_for_phone = State()  # Waiting for user's phone number
    waiting_for_task = State()   # Waiting for project description

# Handle the /start command
@router.message(CommandStart())
async def cmd_start(message: Message):
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🚀 Order Service")]
        ],
        resize_keyboard=True,
        input_field_placeholder="Select an action..."
    )
    
    await message.answer(
        f"Hello, {message.from_user.first_name}!\n\n"
        "Welcome to our CRM Bot. Here you can easily submit a request "
        "for a project cost calculation.\n\n"
        "Click the button below to start.",
        reply_markup=kb
    )

# 1. Triggered when user clicks "🚀 Order Service"
@router.message(F.text == "🚀 Order Service")
async def start_order_form(message: Message, state: FSMContext):
    await state.set_state(OrderForm.waiting_for_name)
    await message.answer(
        "Let's get started! First, please enter your name:",
        reply_markup=ReplyKeyboardRemove()
    )

# 2. Triggered when bot is waiting for name
@router.message(OrderForm.waiting_for_name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(user_name=message.text)
    await state.set_state(OrderForm.waiting_for_phone)
    await message.answer("Thank you! Now, please provide your phone number or telegram handle:")

# 3. Triggered when bot is waiting for phone
@router.message(OrderForm.waiting_for_phone)
async def process_phone(message: Message, state: FSMContext):
    await state.update_data(user_phone=message.text)
    await state.set_state(OrderForm.waiting_for_task)
    await message.answer("Perfect. Finally, please describe your project requirements in a few sentences:")

# 4. Triggered when bot is waiting for task description
@router.message(OrderForm.waiting_for_task)
async def process_task(message: Message, state: FSMContext):
    await state.update_data(user_task=message.text)
    user_data = await state.get_data()
    
    name = user_data.get('user_name')
    contact = user_data.get('user_phone')
    task = user_data.get('user_task')
    
    try:
        await append_lead(name, contact, task)
        sheets_status = "📊 *Saved to CRM spreadsheet!*"
    except Exception as e:
        sheets_status = f"⚠️ *Spreadsheet error:* {e}"

    summary_text = (
        "✅ **Application Successfully Received!**\n\n"
        f"**Name:** {name}\n"
        f"**Contact:** {contact}\n"
        f"**Project Details:** {task}\n\n"
        f"{sheets_status}\n\n"
        "Our manager will contact you shortly. Thank you!"
    )
    
    await message.answer(summary_text, parse_mode="Markdown")
    await state.clear()

# 5. Catch-all handler for any unhandled text messages (ВОЗВРАЩАЕТ КНОПКУ АВТОМАТИЧЕСКИ)
@router.message()
async def fallback_echo(message: Message):
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🚀 Order Service")]
        ],
        resize_keyboard=True,
        input_field_placeholder="Select an action..."
    )
    await message.answer(
        "Please use the button below to start a new project request:",
        reply_markup=kb
    )