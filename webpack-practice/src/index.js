import { greeting } from "./greeting.js";
import "./styles.css";
import myImage from "./image.png";

document.addEventListener("DOMContentLoaded", async () => {
  const message = await new Promise((res, rej) => {
    // setTimeout(() => res("I just loaded mf"), 3000);
    res("I just loaded mf");
  });
  console.log(message);
});

console.log(greeting);

const image = document.createElement("img");
image.src = myImage;

document.body.appendChild(image);
