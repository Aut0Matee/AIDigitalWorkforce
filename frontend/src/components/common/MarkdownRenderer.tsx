import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Typography, Link, Box, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Divider } from '@mui/material';
import { styled } from '@mui/material/styles';

interface MarkdownRendererProps {
  content: string;
}

// Styled components for better markdown rendering
const StyledBlockquote = styled('blockquote')(({ theme }) => ({
  borderLeft: `4px solid ${theme.palette.primary.main}`,
  paddingLeft: theme.spacing(2),
  marginLeft: 0,
  marginRight: 0,
  fontStyle: 'italic',
  color: theme.palette.text.secondary,
}));

const StyledCode = styled('code')(({ theme }) => ({
  backgroundColor: theme.palette.grey[100],
  padding: '2px 6px',
  borderRadius: '4px',
  fontSize: '0.875em',
  fontFamily: 'monospace',
}));

const StyledPre = styled('pre')(({ theme }) => ({
  backgroundColor: theme.palette.grey[900],
  color: theme.palette.common.white,
  padding: theme.spacing(2),
  borderRadius: theme.shape.borderRadius,
  overflowX: 'auto',
  '& code': {
    backgroundColor: 'transparent',
    padding: 0,
    color: 'inherit',
  },
}));

export const MarkdownRenderer: React.FC<MarkdownRendererProps> = ({ content }) => {
  // Ensure content is a string and not undefined/null
  const safeContent = content || '';
  
  try {
    return (
      <ReactMarkdown
      remarkPlugins={[remarkGfm]}
      components={{
        // Headings
        h1: ({ children }) => (
          <Typography variant="h4" component="h1" gutterBottom sx={{ mt: 2, fontWeight: 'bold' }}>
            {children}
          </Typography>
        ),
        h2: ({ children }) => (
          <Typography variant="h5" component="h2" gutterBottom sx={{ mt: 2, fontWeight: 'bold' }}>
            {children}
          </Typography>
        ),
        h3: ({ children }) => (
          <Typography variant="h6" component="h3" gutterBottom sx={{ mt: 1.5, fontWeight: 'bold' }}>
            {children}
          </Typography>
        ),
        h4: ({ children }) => (
          <Typography variant="subtitle1" component="h4" gutterBottom sx={{ mt: 1.5, fontWeight: 'bold' }}>
            {children}
          </Typography>
        ),
        h5: ({ children }) => (
          <Typography variant="subtitle2" component="h5" gutterBottom sx={{ mt: 1, fontWeight: 'bold' }}>
            {children}
          </Typography>
        ),
        h6: ({ children }) => (
          <Typography variant="body1" component="h6" gutterBottom sx={{ mt: 1, fontWeight: 'bold' }}>
            {children}
          </Typography>
        ),
        
        // Paragraphs
        p: ({ children }) => (
          <Typography variant="body2" paragraph sx={{ lineHeight: 1.7 }}>
            {children}
          </Typography>
        ),
        
        // Lists
        ul: ({ children }) => (
          <Box component="ul" sx={{ pl: 3, my: 1 }}>
            {children}
          </Box>
        ),
        ol: ({ children }) => (
          <Box component="ol" sx={{ pl: 3, my: 1 }}>
            {children}
          </Box>
        ),
        li: ({ children }) => (
          <Typography component="li" variant="body2" sx={{ mb: 0.5, lineHeight: 1.7 }}>
            {children}
          </Typography>
        ),
        
        // Links
        a: ({ href, children }) => (
          <Link href={href} target="_blank" rel="noopener noreferrer" underline="hover">
            {children}
          </Link>
        ),
        
        // Code
        code: ({ className, children }) => {
          const isInline = !className;
          
          if (isInline) {
            return <StyledCode>{children}</StyledCode>;
          }
          
          return (
            <StyledPre>
              <code className={className}>{children}</code>
            </StyledPre>
          );
        },
        
        pre: ({ children }) => <StyledPre>{children}</StyledPre>,
        
        // Blockquote
        blockquote: ({ children }) => (
          <StyledBlockquote>
            {children}
          </StyledBlockquote>
        ),
        
        // Horizontal rule
        hr: () => <Divider sx={{ my: 2 }} />,
        
        // Tables (with GFM support)
        table: ({ children }) => (
          <TableContainer component={Paper} variant="outlined" sx={{ my: 2 }}>
            <Table size="small">
              {children}
            </Table>
          </TableContainer>
        ),
        thead: ({ children }) => <TableHead>{children}</TableHead>,
        tbody: ({ children }) => <TableBody>{children}</TableBody>,
        tr: ({ children }) => <TableRow>{children}</TableRow>,
        td: ({ children }) => <TableCell>{children}</TableCell>,
        th: ({ children }) => (
          <TableCell sx={{ fontWeight: 'bold' }}>
            {children}
          </TableCell>
        ),
        
        // Strong and emphasis
        strong: ({ children }) => (
          <Typography component="span" sx={{ fontWeight: 'bold' }}>
            {children}
          </Typography>
        ),
        em: ({ children }) => (
          <Typography component="span" sx={{ fontStyle: 'italic' }}>
            {children}
          </Typography>
        ),
      }}
    >
      {safeContent}
    </ReactMarkdown>
    );
  } catch (error) {
    console.error('Error rendering markdown:', error);
    // Fallback to plain text with preserved formatting
    return (
      <Typography variant="body2" component="div" sx={{ whiteSpace: 'pre-wrap' }}>
        {safeContent}
      </Typography>
    );
  }
};