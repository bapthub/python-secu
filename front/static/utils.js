function submitFormHandler(formId, onSubmitCallback)
{
    const form = document.getElementById(formId);

    form.addEventListener('submit', async event => {
        event.preventDefault();

        const data = new FormData(form);

        console.log(Array.from(data));

        await onSubmitCallback(data);
    });
}