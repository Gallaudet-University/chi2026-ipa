let Keyboard = window.SimpleKeyboard.default;
let keyboard = new Keyboard({
    onChange: input => onChange(input),
    onKeyPress: button => onKeyPress(button),
});

var user_input_ = document.querySelector('.user-input');
user_input_.style.opacity = 0;

document.querySelector('.keyboard').addEventListener('click', () => {
    let user_input = document.getElementById('user_input');
    let keyboardElement = document.querySelector('.simple-keyboard');

    // 切换键盘显示/隐藏
    if (keyboardElement.style.display === 'none' || !keyboardElement.style.display) {
        // 如果键盘内容是空的，则设置输入框
        if (keyboardElement.innerHTML === '') {
            user_input.disabled = false;
            user_input.focus();
            // 将光标移到输入框末尾
            user_input.setSelectionRange(user_input.value.length, user_input.value.length);
            keyboard.setInput(user_input.value);  // 初始化键盘内容
        }
        // 显示键盘
        keyboardElement.style.display = 'block';
        user_input.disabled = false;  // 解锁输入框
        user_input_.style.opacity = 1;
        user_input.focus();
        user_input.setSelectionRange(user_input.value.length, user_input.value.length);  // 光标定位到末尾
    } else {
        // 隐藏键盘
        keyboardElement.style.display = 'none';
        user_input_.style.opacity = 0;
        user_input.disabled = true;  // 禁用输入框
    }
});
let currentInput = document.getElementById('user_input').value;
function onChange(input) {
    document.getElementById('user_input').value = currentInput + input;
}

function onKeyPress(button) {
    if (button === "{shift}" || button === "{lock}") handleShift();
    if (button === "{enter}") {
        let user_input = document.getElementById('user_input').value;
        window.location.href = `/customcommand?task=${user_input}`;
    }
    if (button === "{bksp}") {
        theContentThatHasAlreadyBeenEntered = keyboard.getInput();
        keyboard.setInput(theContentThatHasAlreadyBeenEntered.slice(0, -1));
        document.getElementById('user_input').value = currentInput + keyboard.getInput();
        if (theContentThatHasAlreadyBeenEntered.length === 0) {
            // 删除currentInput最后一个字符
            currentInput = currentInput.slice(0, -1);
            document.getElementById('user_input').value = currentInput;
        }
    }
}

function handleShift() {
    let currentLayout = keyboard.options.layoutName;
    let shiftToggle = currentLayout === "default" ? "shift" : "default";
    keyboard.setOptions({
        layoutName: shiftToggle
    });
}