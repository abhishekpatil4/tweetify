const driverObjSettingsPageConfig = {
    showProgress: true,
    steps: [
        {
            element: '#connect-accounts-section',
            popover: {
                title: 'Connect Accounts',
                description: 'Add your Composio API key and connect your Twitter account to get started.'
            }
        },
        {
            element: '#add-new-user-section',
            popover: {
                title: 'Add New User',
                description: 'Enter twitter username to add new user'
            }
        },
    ]
};

export { driverObjSettingsPageConfig };
