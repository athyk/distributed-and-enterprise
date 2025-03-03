<script lang="ts">
	let email = '';
	let password = '';

	import Input from '$components/FormInput/Input.svelte';

	function handleLogin() {
		console.log('Email:', email);
		console.log('Password:', password);
	}
</script>

<div
	class="mx-auto mt-5 flex w-1/2 overflow-hidden rounded-lg border-1 border-black bg-white shadow-lg"
>
	<div
		class="hidden w-1/2 bg-cover md:block"
		style="background-image: url('https://images.unsplash.com/photo-1521587760476-6c12a4b040da?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D')"
	></div>
	<div class="w-full p-8 md:w-1/2">
		<h2 class="text-center text-2xl font-semibold text-gray-700">Login</h2>
		<p class="text-center text-xl text-gray-600">Welcome back!</p>
		<form on:submit|preventDefault={handleLogin}>
			<Input
				Name="Email"
				placeholder="Enter your email"
				type="email"
				showLabel={true}
				bind:value={email}
			/>
			<Input
				Name="Password"
				placeholder="Enter your password"
				type="password"
				showLabel={true}
				bind:value={password}
			/>
			<div
				class="mt-4 flex flex-col items-center justify-between space-y-2 md:flex-row md:space-y-0"
			>
				<button type="submit" class="rounded-lg bg-blue-600 px-6 py-2 text-white hover:bg-blue-900"
					>Login</button
				>
				<a href="/register" class="text-sm text-gray-600 hover:text-gray-900">Not got an Account?</a
				>
			</div>
		</form>
	</div>
</div>
