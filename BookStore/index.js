let library;

if (localStorage.getItem("library")) {
  library = JSON.parse(localStorage.getItem("library"));
} else {
  library = [];
}

let len = library.length;
console.log(len);

const bookContainer = document.querySelector(".container");
const plus = document.querySelector("#addBook");

plus.style.color = "red";
plus.style.cursor = "pointer";
plus.addEventListener("click", () => {
  addBook("Misk Love", "JDD", "500", false);
});

// add book
function addBook() {
  // add book
  const [name, author, pageNumbers, read] = arguments;
  console.log(...arguments, "arguments");

  library.push({ name, author, pageNumbers, read });
  console.log(library, "library");

  localStorage.setItem("library", JSON.stringify(library));
  location.reload();
}

// create book
function createBook() {
  const [name, author, pageNumbers, read] = arguments;
  // create book content
  let book = document.createElement("div");
  let bookname = document.createElement("p");
  let bookauthor = document.createElement("p");
  let bookpages = document.createElement("p");
  let bookread = document.createElement("p");
  // add content
  bookname.innerHTML = `${name}`;
  bookauthor.innerHTML = `${author}`;
  bookpages.innerHTML = `${pageNumbers}`;
  bookread.innerHTML = `${read}`;
  // apend content to book
  book.appendChild(bookname);
  book.appendChild(bookauthor);
  book.appendChild(bookpages);
  book.appendChild(bookread);

  book.classList.add("card");
  return book;
}
for (let i = 0; i < library.length; i++) {
  // push item to dom
  bookContainer.appendChild(createBook(...Object.values(library[i])));
}
// load library
