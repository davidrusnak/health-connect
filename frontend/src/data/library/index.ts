export interface EduResource {
    fileId: string;
    type: 'html' | 'link_pdf' | 'link_external';
    title: string;
    topics: string[];
    authors?: string[];
    dateCreated: string;
    content?: string;
};