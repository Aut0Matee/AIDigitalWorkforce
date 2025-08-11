import React from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  IconButton,
  Typography,
  Box
} from '@mui/material';
import {
  Close as CloseIcon,
  PictureAsPdf as PDFIcon,
  Code as CodeIcon,
  Download as DownloadIcon
} from '@mui/icons-material';
import jsPDF from 'jspdf';

interface ExportModalProps {
  isOpen: boolean;
  onClose: () => void;
  content: string;
  title: string;
}

export const ExportModal: React.FC<ExportModalProps> = ({ isOpen, onClose, content, title }) => {
  const handleExportPDF = () => {
    const pdf = new jsPDF();
    const pageHeight = pdf.internal.pageSize.getHeight();
    const pageWidth = pdf.internal.pageSize.getWidth();
    const margin = 20;
    const lineHeight = 7;
    let y = margin;

    // Add title
    pdf.setFontSize(16);
    pdf.text(title, margin, y);
    y += lineHeight * 2;

    // Add content
    pdf.setFontSize(11);
    const lines = pdf.splitTextToSize(content, pageWidth - 2 * margin);
    
    lines.forEach((line: string) => {
      if (y + lineHeight > pageHeight - margin) {
        pdf.addPage();
        y = margin;
      }
      pdf.text(line, margin, y);
      y += lineHeight;
    });

    pdf.save(`${title.replace(/[^a-z0-9]/gi, '_').toLowerCase()}.pdf`);
    onClose();
  };

  const handleExportMarkdown = () => {
    const blob = new Blob([content], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${title.replace(/[^a-z0-9]/gi, '_').toLowerCase()}.md`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    onClose();
  };

  return (
    <Dialog
      open={isOpen}
      onClose={onClose}
      maxWidth="sm"
      fullWidth
    >
      <DialogTitle>
        <Box display="flex" justifyContent="space-between" alignItems="center">
          Export Deliverable
          <IconButton
            edge="end"
            color="inherit"
            onClick={onClose}
            aria-label="close"
          >
            <CloseIcon />
          </IconButton>
        </Box>
      </DialogTitle>
      <DialogContent>
        <Typography variant="body2" color="text.secondary" gutterBottom>
          Choose a format to export your deliverable:
        </Typography>
        
        <List sx={{ mt: 2 }}>
          <ListItem disablePadding>
            <ListItemButton onClick={handleExportPDF}>
              <ListItemIcon>
                <PDFIcon color="error" />
              </ListItemIcon>
              <ListItemText
                primary="PDF Document"
                secondary="Download as PDF file"
              />
              <DownloadIcon color="action" />
            </ListItemButton>
          </ListItem>
          
          <ListItem disablePadding>
            <ListItemButton onClick={handleExportMarkdown}>
              <ListItemIcon>
                <CodeIcon />
              </ListItemIcon>
              <ListItemText
                primary="Markdown"
                secondary="Download as .md file"
              />
              <DownloadIcon color="action" />
            </ListItemButton>
          </ListItem>
        </List>
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Cancel</Button>
      </DialogActions>
    </Dialog>
  );
};