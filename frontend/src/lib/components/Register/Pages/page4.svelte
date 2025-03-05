<script lang="ts">
	export let otp: string[] = [];
</script>

<h1 class="mt-4 mb-3 text-2xl font-bold">Enter the code sent to your email</h1>
<div class="flex flex-row justify-center">
	{#each Array.from({ length: 6 }) as _, i}
		<input
			type="text"
			class="mt-2 mr-2 w-[45px] rounded-md border px-4 py-2 focus:ring-1 focus:ring-blue-600 focus:outline-none"
			inputmode="numeric"
			maxlength="1"
			on:keyup={() => {
				if (otp[i].length == 1) document.querySelectorAll('input')[i + 1]?.focus();
			}}
			bind:value={otp[i]}
		/>
	{/each}
</div>
