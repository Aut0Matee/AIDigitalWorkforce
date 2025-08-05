import React from 'react';
import { X, Download, FileText, FileCode } from 'lucide-react';
import jsPDF from 'jspdf';

interface ExportModalProps {
  isOpen: boolean;
  onClose: () => void;
  content: string;
  title: string;
}

export const ExportModal: React.FC<ExportModalProps> = ({ isOpen, onClose, content, title }) => {
  if (!isOpen) return null;

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
  };

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto">
      <div className="flex items-center justify-center min-h-screen px-4 pt-4 pb-20 text-center sm:block sm:p-0">
        <div className="fixed inset-0 transition-opacity bg-gray-500 bg-opacity-75" onClick={onClose} />

        <div className="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
          <div className="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-medium text-gray-900">Export Deliverable</h3>
              <button
                onClick={onClose}
                className="text-gray-400 hover:text-gray-500 focus:outline-none"
              >
                <X className="h-5 w-5" />
              </button>
            </div>

            <p className="text-sm text-gray-600 mb-6">
              Choose a format to export your deliverable:
            </p>

            <div className="space-y-3">
              <button
                onClick={handleExportPDF}
                className="w-full flex items-center justify-between px-4 py-3 border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-primary-500"
              >
                <div className="flex items-center space-x-3">
                  <FileText className="h-5 w-5 text-red-600" />
                  <div className="text-left">
                    <p className="text-sm font-medium text-gray-900">PDF Document</p>
                    <p className="text-xs text-gray-500">Download as PDF file</p>
                  </div>
                </div>
                <Download className="h-4 w-4 text-gray-400" />
              </button>

              <button
                onClick={handleExportMarkdown}
                className="w-full flex items-center justify-between px-4 py-3 border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-primary-500"
              >
                <div className="flex items-center space-x-3">
                  <FileCode className="h-5 w-5 text-gray-600" />
                  <div className="text-left">
                    <p className="text-sm font-medium text-gray-900">Markdown</p>
                    <p className="text-xs text-gray-500">Download as .md file</p>
                  </div>
                </div>
                <Download className="h-4 w-4 text-gray-400" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};