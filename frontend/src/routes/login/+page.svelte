<script lang="ts">
	import AccountCard from '$components/AccountCard/base.svelte';
	import Page from '$components/AccountCard/RegisterPages/page.svelte';
	import { post } from '$lib/api/post';
	import type { RegiserResponse } from '$lib/api/apiType';

	let errorMessage = "";
	let email: [string, string, string] = ['','Email',"Enter your email"]
	let password: [string, string, string] = ['','Password',"Enter your password"]

	async function register() {
		if (email[0] === "" || password[0] === "") {
			errorMessage = "Please fill in all fields";
			return;
		}
		if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email[0])) {
			errorMessage = "Invalid email format";
			return;
		}
		let data = {
			"email": email[0],
			"password": password[0],
		};
		let response = (await post('auth/login', data)) as RegiserResponse;
		if (response.success) {
			errorMessage = "";
			window.location.href = "/";
		} else {
			errorMessage = "";
			for (let i = 0; i < response.error_message.length; i++) {
				if (i > 0) {
					errorMessage += " | ";
				}
				errorMessage += response.error_message[i];
			}
		}
	}

</script>


<div class="flex h-screen w-full items-center justify-center">
	<AccountCard
		title="Login"
		subText="Login to your account"
		imageUrl="https://images.unsplash.com/photo-1521587760476-6c12a4b040da?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
		promoteUrl="register"
		promoteText="Don't have an account?"
		maxstep={1}
		submitFunction={register}
		bind:errorMessage
	>
		<svelte:fragment slot="pages">
			<div class="p-15">
			<Page
				bind:email
				bind:password
			/>
			</div>
		</svelte:fragment>
	</AccountCard>
</div>