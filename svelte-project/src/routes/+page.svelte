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
  
<div class="container">
	<div class="login-card">
		<h2>🔑 Login</h2>
		<input type="text" bind:value={initials} placeholder="Enter Initials" />
		<div class="checkbox-container">
			<label>
				<input type="checkbox" bind:checked={isLead} />
				Lead Analyst?
			</label>
		</div>
		<button on:click={login}>Login</button>
	</div>
</div>
  
<style>
	/* Global styles */
	body {
		margin: 0;
		padding: 0;
		font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
		background: linear-gradient(135deg, #74ebd5 0%, #9face6 100%);
	}
  
	/* Container centers the login card */
	.container {
		display: flex;
		align-items: center;
		justify-content: center;
		min-height: 100vh;
		padding: 1rem;
	}
  
	/* Login card styles */
	.login-card {
		background-color: #ffffff;
		padding: 2rem;
		border-radius: 10px;
		box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
		max-width: 400px;
		width: 100%;
		text-align: center;
	}
  
	h2 {
		margin-bottom: 1.5rem;
		color: #333;
	}
  
	input[type="text"] {
		width: 100%;
		padding: 0.75rem;
		margin-bottom: 1rem;
		border: 1px solid #ddd;
		border-radius: 5px;
		font-size: 1rem;
	}
  
	.checkbox-container {
		margin-bottom: 1.5rem;
		text-align: left;
	}
  
	.checkbox-container label {
		font-size: 1rem;
		color: #555;
	}
  
	button {
		background-color: #74ebd5;
		border: none;
		color: #fff;
		padding: 0.75rem 1.5rem;
		font-size: 1rem;
		border-radius: 5px;
		cursor: pointer;
		transition: background-color 0.3s ease;
	}
  
	button:hover {
		background-color: #68c3ac;
	}
</style>
