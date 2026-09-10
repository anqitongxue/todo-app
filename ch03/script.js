// 选中页面元素
const input = document.querySelector(".input");
const button = document.querySelector(".btn");
const list = document.querySelector(".list");

// 内存里的任务列表（刷新页面就没了，第 6 章会存进数据库）
const tasks = [];

// 从输入框取文字，添加一条任务（按钮点击 和 按回车 都调用它）
function addFromInput() {
    const text = input.value;
    if (text === "") {
        return;
    }
    tasks.push(text);   // 存进内存
    addTask(text);      // 把"造一项并挂到页面"交给下面的函数去做
    input.value = "";   // 清空输入框
}

// 点击"添加"按钮 → 添加
button.addEventListener("click", addFromInput);

// 在输入框里按回车（Enter）→ 也添加
input.addEventListener("keydown", function (event) {
    if (event.key === "Enter") {
        addFromInput();
    }
});

// 新增一个任务：造一个 <li>（文字 + 删除按钮），挂到 <ul> 下面
function addTask(text) {
    const li = document.createElement("li");

    // 1) 文字部分：用一个 <span> 装任务文字
    const span = document.createElement("span");
    span.textContent = text;
    li.appendChild(span);

    // 2) 删除按钮部分
    const delBtn = document.createElement("button");
    delBtn.textContent = "删除";
    delBtn.className = "del";    // 给按钮加 class="del"，方便 CSS 美化

    // 给删除按钮绑定点击事件：
    // 这个函数"记住"了自己属于哪个 li、对应哪段文字（这叫"闭包"），
    // 所以每个按钮都能精确删掉自己那一项。
    delBtn.addEventListener("click", function () {
        li.remove();                       // ① 从页面上删掉这一项
        const index = tasks.indexOf(text); // ② 在数组里找这段文字的位置
        if (index !== -1) {                // 找到了（不等于 -1）
            tasks.splice(index, 1);        // ③ 从数组里删掉它
        }
    });
    li.appendChild(delBtn);

    // 把整个 <li> 挂到 <ul> 下面
    list.appendChild(li);
}
