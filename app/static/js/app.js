// app/static/js/app.js
const API_BASE = "/api";

function setToken(token) {
  localStorage.setItem("jwt", token);
}
function getToken() {
  return localStorage.getItem("jwt");
}
function clearToken() {
  localStorage.removeItem("jwt");
}
function authHeader() {
  return { Authorization: `Bearer ${getToken()}` };
}

document.addEventListener("DOMContentLoaded", () => {
  const path = window.location.pathname;

  const profileLink = document.getElementById("profile-link");
  if (profileLink) {
    const token = getToken();
    if (token) {
      const payload = JSON.parse(
        atob(token.split(".")[1].replace(/-/g, "+").replace(/_/g, "/"))
      );
      const userId = payload.sub || payload.identity;
      profileLink.href = `/users/${userId}`;
      profileLink.style.display = "block";
    }
  }

  if (path === "/register") {
    document.getElementById("register-form").onsubmit = async (e) => {
      e.preventDefault();
      const f = e.target;
      const res = await fetch(API_BASE + "/users/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          username: f.username.value,
          email: f.email.value,
          password: f.password.value,
        }),
      });
      if (res.ok) window.location = "/login";
      else alert("Registration failed");
    };
  }

  if (path === "/login") {
    document.getElementById("login-form").onsubmit = async (e) => {
      e.preventDefault();
      const f = e.target;
      const res = await fetch(API_BASE + "/users/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          email: f.email.value,
          password: f.password.value,
        }),
      });
      if (res.ok) {
        const { access_token } = await res.json();
        setToken(access_token);
        window.location = "/events";
      } else alert("Login failed");
    };
  }

  if (path === "/events") {
    document.getElementById("create-event-form").onsubmit = async (e) => {
      e.preventDefault();
      const f = e.target;
      const res = await fetch(API_BASE + "/events/", {
        method: "POST",
        headers: { "Content-Type": "application/json", ...authHeader() },
        body: JSON.stringify({
          title: f.title.value,
          datetime: f.datetime.value,
          location: f.location.value,
          description: f.description.value,
        }),
      });
      if (res.ok) window.location.reload();
      else alert("Create failed");
    };

    document.querySelectorAll(".rsvp-btn").forEach((btn) => {
      btn.onclick = async () => {
        const id = btn.dataset.id;
        await fetch(`${API_BASE}/events/${id}/register`, {
          method: "POST",
          headers: authHeader(),
        });
        btn.textContent = "Attending";
        btn.disabled = true;
      };
    });
  }

  if (/^\/events\/\d+$/.test(path)) {
    document.getElementById("rsvp-button").onclick = async () => {
      const id = path.split("/").pop();
      await fetch(`${API_BASE}/events/${id}/register`, {
        method: "POST",
        headers: authHeader(),
      });
      alert("You are now attending!");
    };
  }

  if (/^\/users\/\d+$/.test(path)) {
    const logoutForm = document.getElementById("logout-form");
    if (logoutForm) {
      logoutForm.onsubmit = (e) => {
        e.preventDefault();
        clearToken();
        window.location = "/login";
      };
    }
  }
});
