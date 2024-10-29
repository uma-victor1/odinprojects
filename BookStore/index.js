const bookContainer = document.querySelector(".container");
const dialog = document.getElementById("bookDialog");
const openDialogBtn = document.getElementById("openDialogBtn");

const closeDialogBtn = document.getElementById("closeDialogBtn");
const form = document.getElementById("bookForm");
const plus = document.querySelector("#addBook");
const addBookCard = document.createElement("div");
addBookCard.classList.add("card");
addBookCard.appendChild(plus);
closeDialogBtn.addEventListener("click", () => {
  dialog.close();
});
let library = [];

function Book() {
  const [name, author, pageNumbers, read] = arguments;

  this.id = Math.floor(Math.random() * 1000);
  this.name = name;
  this.author = author;
  this.pageNumbers = pageNumbers;
  this.read = read;
}
// add toogle read function to prototype
Book.prototype.toggleRead = function (e) {
  let bookId = Number(e.target.parentElement.dataset.id);
  library = library.map((lib) => {
    if (lib.id === bookId) {
      return { ...lib, read: !lib.read };
    }
    return lib;
  });
  loadLibrary();
};

// add event listener add book box
addBookCard.addEventListener("click", () => {
  showModal();
});

// add click event listener to form
form.addEventListener("submit", (e) => {
  e.preventDefault();
  addBook(
    form.bookName.value,
    form.author.value,
    form.pageNumbers.value,
    form.read.checked
  );
  form.reset();
  dialog.close();
});

// show modal
function showModal() {
  dialog.showModal();
  return;
}

// add book
function addBook() {
  const [name, author, pageNumbers, read] = arguments;

  library.push(new Book(...arguments));

  loadLibrary();
}

// create book
function createBook() {
  const [id, name, author, pageNumbers, read] = arguments;
  console.log(arguments);

  // create book content
  let book = document.createElement("div");
  let bookname = document.createElement("p");
  let bookauthor = document.createElement("p");
  let bookpages = document.createElement("p");
  let bookread = document.createElement("p");
  let delButton = document.createElement("button");
  let toggleButton = document.createElement("button");

  book.setAttribute("data-id", `${id}`);
  delButton.innerHTML = "Delete";
  delButton.addEventListener("click", function (e) {
    let bookId = Number(e.target.parentElement.dataset.id);
    console.log(library, "libraryxx");

    library = library.filter((lib) => {
      console.log(bookId, lib.id);
      return lib.id !== bookId;
    });

    loadLibrary();
  });

  toggleButton.innerHTML = "Toggle Read";
  toggleButton.addEventListener("click", Book.prototype.toggleRead);

  // add content
  bookname.innerHTML = `Name: ${name}`;
  bookauthor.innerHTML = `Author: ${author}`;
  bookpages.innerHTML = `Pages: ${pageNumbers}`;
  bookread.innerHTML = `Read: ${read}`;

  // apend content to book
  book.appendChild(bookname);
  book.appendChild(bookauthor);
  book.appendChild(bookpages);
  book.appendChild(bookread);
  book.appendChild(delButton);
  book.appendChild(toggleButton);

  book.classList.add("card");
  return book;
}

// load library
function loadLibrary() {
  bookContainer.innerHTML = "";
  bookContainer.appendChild(addBookCard);
  for (let i = 0; i < library.length; i++) {
    // push item to dom
    bookContainer.appendChild(createBook(...Object.values(library[i])));
    console.log(library, "mylibrary");
  }
}

loadLibrary();
