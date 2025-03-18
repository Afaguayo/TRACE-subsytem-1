<script>
	import { goto } from "$app/navigation";
  
	let initials = "";
	let isLead = false;
	let user = null;
  
	async function login() {
	  const response = await fetch("http://localhost:5001/login", {
		method: "POST",
		headers: { "Content-Type": "application/json" },
		body: JSON.stringify({ initials, is_lead: isLead }),
	  });
  
	  if (response.ok) {
		user = await response.json();
		localStorage.setItem("user", JSON.stringify(user));
		goto("/dashboard"); // Redirect to dashboard after login
	  }
	}
  </script>
  
  <div class="login">
	<h2>🔑 Login</h2>
	<input type="text" bind:value={initials} placeholder="Enter Initials" />
	<label>
	  <input type="checkbox" bind:checked={isLead} />
	  Lead Analyst?
	</label>
	<button on:click={login}>Login</button>
  </div>
  