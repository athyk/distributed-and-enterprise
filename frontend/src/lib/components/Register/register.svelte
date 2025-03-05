<script lang="ts">
	import Input from '$components/FormInput/Input.svelte';
	import Button from '$components/SubmitButton/button.svelte';
	import Page1 from './Pages/page1.svelte';
	import Page2 from './Pages/page2.svelte';
	import Page3 from './Pages/page3.svelte';
	import Page4 from './Pages/page4.svelte';

	let email = '';
	let password = '';
	let passwordConfirm = '';

	let fName = '';
	let lName = '';
	let dob = '';
	let gender = '';

	let degree = '';
	let degreeYear = '';
	let graduationYear = '';

	let tags = '';

	let otp: string[] = [];

	let step = 1;
	let maxstep = 4;

	let page1Inputs: Input[] = [];
	let page2Inputs: Input[] = [];
	let page3Inputs: Input[] = [];

	let pageInputs = [page1Inputs, page2Inputs, page3Inputs];

	function checkPageValidity() {
		let valid = true;
		pageInputs[step - 1].forEach((input) => {
			if (!input.reportValidity()) {
				console.log('Not VALID!!!! :(');
				valid = false;
			}
		});
		console.log('Page Valid: ', valid);
		if (step === 1 && valid) {
			valid = password === passwordConfirm;
			console.log('Password Match: ', valid);
			page1Inputs[1].setErrorMessage("Password doesn't match");
			page1Inputs[2].setErrorMessage("Password doesn't match");
		}
		console.log('Password Valid: ', valid);
		if (valid) {
			step = Math.min(maxstep, step + 1);
		}
		console.log(valid);
		return valid;
	}

	function handleSubmit() {
		let data = {
			email,
			password,
			passwordConfirm,
			fName,
			lName,
			dob,
			gender,
			degree,
			degreeYear,
			graduationYear,
			tags
		};
		console.log(data);
	}
</script>


<div class="w-full p-8 md:w-1/2 md:mx-auto">
	<h2 class="text-center text-2xl font-semibold text-gray-700">Register</h2>
	<p class="text-center text-xl text-gray-600">Fill in User Info</p>
	<form on:submit|preventDefault={handleSubmit}>
		{#if step === 1}
			<Page1 bind:email bind:password bind:passwordConfirm bind:pageInputs={page1Inputs} />
		{/if}

		{#if step === 2}
			<Page2 bind:fName bind:lName bind:dob bind:pageInputs={page2Inputs} />
		{/if}

		{#if step === 3}
			<Page3 bind:degree bind:degreeYear bind:graduationYear bind:tags bind:pageInputs={page3Inputs} />
		{/if}
		{#if step === 4}
			<Page4 bind:otp={otp} />
		{/if}

		<div class="mt-4 flex flex-col items-center justify-between space-y-2 md:flex-row md:space-y-0">
			{#if step === 1}
				<a href="/login" class="text-sm text-gray-600 hover:text-gray-900"
					>Already have an Account?</a
				>
			{/if}
			{#if step > 1}
				<Button type="button" text="Previous Step" on:click={() => (step = Math.max(1, step - 1))} />
			{/if}

			{#if step === maxstep}
				<Button/>
			{:else}
				<Button type="button" text="Next Step" onClick={checkPageValidity} />
			{/if}

		</div>
	</form>
</div>
