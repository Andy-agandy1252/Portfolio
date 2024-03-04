document.addEventListener('DOMContentLoaded', function () {
  window.addEventListener('scroll', function () {
    var scrollPosition = window.scrollY || document.documentElement.scrollTop;

    var offset = 100;

    var sections = document.querySelectorAll("section");
    var currentSectionId = null;

    sections.forEach(function (section) {
      var sectionTop = section.offsetTop - offset;
      var sectionBottom = sectionTop + section.offsetHeight;

      if (scrollPosition >= sectionTop && scrollPosition < sectionBottom) {
        currentSectionId = section.id;
      }
    });

    updateActiveState(currentSectionId);
  });
});

function updateActiveState(sectionId) {
  var navLinks = document.querySelectorAll('.topnav .right-links a');
  navLinks.forEach(function (link) {
    link.classList.remove('active');
  });

  var currentNavLink = document.querySelector(`.topnav .right-links a[onclick*="${sectionId}"]`);
  if (currentNavLink) {
    currentNavLink.classList.add('active');
  }

  var highlightLine = document.querySelector('.highlight-line');
  if (highlightLine && currentNavLink) {
    var rect = currentNavLink.getBoundingClientRect();
    var x = rect.left + window.scrollX;
    highlightLine.style.transform = `translateX(${x}px)`;
  }
}

function scrollToSection(sectionId) {
  var targetSection = document.getElementById(sectionId);
  if (targetSection) {
    targetSection.scrollIntoView({ behavior: 'smooth' });
  }
}

function myFunction() {
  var x = document.getElementById("myTopnav");
  if (x.className === "topnav") {
    x.className += " responsive";
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
  } else {
    x.className = "topnav";
  }

  updateActiveState(getCurrentSectionId());
}

function getCurrentSectionId() {
  // Logic to determine the current section ID dynamically
  var sections = document.querySelectorAll("section");
  var currentSectionId = null;

  sections.forEach(function (section) {
    var rect = section.getBoundingClientRect();
    var sectionCenter = rect.left + rect.width / 2;

    if (sectionCenter >= 0 && sectionCenter <= window.innerWidth) {
      currentSectionId = section.id;
    }
  });

  return currentSectionId;
}

/*--------------------*/
document.addEventListener('DOMContentLoaded', function () {
    var messagesContainer = document.getElementById('messages-container');

    function removeMessage() {
        var successMessage = document.getElementById('successMessage');

        if (successMessage) {
            // Add the 'fade-out' class to trigger the fade-out animation
            successMessage.classList.add('fade-out');
        }
    }

    // Remove the message when the 'transitionend' event occurs
    function handleTransitionEnd(event) {
        if (event.propertyName === 'opacity') {
            messagesContainer.removeChild(successMessage);
        }
    }

    // Call the function when the DOM is loaded
    removeMessage();

});
/*-----------*/
// Function to scroll to a specific section from HOME SECTION
function scrollToSection(sectionId, event) {
  if (event) {
    event.preventDefault(); // Check if event is provided before calling preventDefault
  }
  var targetSection = document.getElementById(sectionId);
  if (targetSection) {
    targetSection.scrollIntoView({ behavior: 'smooth' });
  }
}

// Function to scroll specifically to the home section
function scrollToHome(event) {
  if (event) {
    event.preventDefault();
  }
  var homeSection = document.getElementById('home');
  if (homeSection) {
    homeSection.scrollIntoView({ behavior: 'smooth' });
  }
}

document.addEventListener('DOMContentLoaded', function () {
  // Your existing code here

  // Update the home link to use scrollToHome function
  var homeLink = document.querySelector('.home-link');
  if (homeLink) {
    homeLink.addEventListener('click', function (event) {
      scrollToHome(event);
    });
  }
});
