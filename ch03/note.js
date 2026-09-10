// 这是我们的第一个 JS 文件。
// 浏览器会按从上到下的顺序，一行行执行这些代码。

// 1. 变量：给数据起个名字，方便反复使用
let task = "学 JavaScript";   // let 声明一个"可以改"的变量
const year = 2026;           // const 声明一个"不能改"的常量
let name = "苹果"
let time = 20260910

// 2. 数组：用方括号 [ ] 装一列数据
let tasks = ["学 HTML", "学 CSS", "学 JavaScript"];

// 3. 对象：用花括号 { } 装"带名字"的数据（名字: 值）
let todo = { name: "学 JS", done: false };

// 4. 函数：一段可以反复调用的代码
function sayHello() {
    console.log("你好，控制台！");
}

// 下面把上面这些东西打印到控制台，看看它们长什么样
console.log(task);
console.log(year);
console.log(tasks);
console.log(todo);
console.log(name,time)
sayHello();
