import * as vscode from 'vscode';

export function activate(context: vscode.ExtensionContext) {
    let generateTest = vscode.commands.registerCommand(
        'qa-automation.generateTest',
        async () => {
            const editor = vscode.window.activeTextEditor;
            if (!editor) return;

            const selection = editor.selection;
            const selectedCode = editor.document.getText(selection);

            try {
                const response = await fetch('http://localhost:8000/api/ai/generate-test', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ code: selectedCode })
                });

                const result = await response.json();
                editor.edit(editBuilder => {
                    editBuilder.insert(selection.end, '\n\n' + result.test_code);
                });
                vscode.window.showInformationMessage('Test generated successfully!');
            } catch (error) {
                vscode.window.showErrorMessage('Failed to generate test');
            }
        }
    );

    context.subscriptions.push(generateTest);
}

export function deactivate() {}
