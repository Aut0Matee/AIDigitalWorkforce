import React from 'react';
import { Box, Typography, Paper } from '@mui/material';
import ReactMarkdown from 'react-markdown';

export const TestMarkdown: React.FC = () => {
  const testContent = `
# Test Heading 1
## Test Heading 2

This is a **bold** text and this is *italic*.

- List item 1
- List item 2
- List item 3

\`\`\`javascript
const test = "Hello World";
console.log(test);
\`\`\`

[Link to Google](https://google.com)
`;

  return (
    <Paper sx={{ p: 3, m: 2 }}>
      <Typography variant="h6" gutterBottom>Markdown Test</Typography>
      <Box sx={{ border: '1px solid #ccc', p: 2, borderRadius: 1 }}>
        <ReactMarkdown>{testContent}</ReactMarkdown>
      </Box>
    </Paper>
  );
};