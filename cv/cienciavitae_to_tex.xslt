<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" 
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:cv="http://www.cienciavitae.pt/ns/person-extended"
    xmlns:curriculum="http://www.cienciavitae.pt/ns/curriculum"
    xmlns:output="http://www.cienciavitae.pt/ns/output"
    xmlns:service="http://www.cienciavitae.pt/ns/service"
    xmlns:distinction="http://www.cienciavitae.pt/ns/distinction"
    xmlns:common="http://www.cienciavitae.pt/ns/common"
    xmlns:person-info="http://www.cienciavitae.pt/ns/person-info"
    xmlns:identifying-info="http://www.cienciavitae.pt/ns/identifying-info"
    xmlns:resume="http://www.cienciavitae.pt/ns/resume"
    xmlns:email="http://www.cienciavitae.pt/ns/email"
    xmlns:extra="http://extra">
  
  <xsl:output method="text" encoding="UTF-8"/>
  
  <xsl:template match="/">
    <xsl:text>\documentclass[11pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[margin=2.5cm]{geometry}
\usepackage{enumitem}
\usepackage{hyperref}

\title{Curriculum Vitae}
\author{</xsl:text>
    <xsl:value-of select="curriculum:curriculum/identifying-info:identifying-info/person-info:person-info/person-info:full-name"/>
    <xsl:text>}
\date{}

\begin{document}

\maketitle

\section{Personal Information}
\begin{itemize}[leftmargin=*]
  \item \textbf{Name:} </xsl:text>
    <xsl:call-template name="escape-latex">
      <xsl:with-param name="text" select="curriculum:curriculum/identifying-info:identifying-info/person-info:person-info/person-info:full-name"/>
    </xsl:call-template>
    <xsl:text>
  \item \textbf{Email:} </xsl:text>
    <xsl:value-of select="curriculum:curriculum/identifying-info:identifying-info/email:emails/email:email[@preferred-email='true']/email:email-address"/>
    <xsl:text>
\end{itemize}

</xsl:text>
    <xsl:if test="curriculum:curriculum/identifying-info:identifying-info/resume:resume">
      <xsl:text>\section{About}
</xsl:text>
      <xsl:call-template name="escape-latex">
        <xsl:with-param name="text" select="curriculum:curriculum/identifying-info:identifying-info/resume:resume"/>
      </xsl:call-template>
      <xsl:text>

</xsl:text>
    </xsl:if>
    <xsl:text>\section{Publications}

\subsection{Journal Articles}
\begin{enumerate}[leftmargin=*]
</xsl:text>
    <xsl:apply-templates select="curriculum:curriculum/output:outputs/output:output[output:journal-article]">
      <xsl:sort select="output:*/output:publication-date/@year | output:*/output:publication-year" order="descending"/>
    </xsl:apply-templates>
    <xsl:text>\end{enumerate}

\subsection{Conference Papers}
\begin{enumerate}[leftmargin=*]
</xsl:text>
    <xsl:apply-templates select="curriculum:curriculum/output:outputs/output:output[output:conference-paper]">
      <xsl:sort select="output:*/output:publication-date/@year | output:*/output:presentation-date/@year" order="descending"/>
    </xsl:apply-templates>
    <xsl:text>\end{enumerate}

\subsection{Conference Posters}
\begin{enumerate}[leftmargin=*]
</xsl:text>
    <xsl:apply-templates select="curriculum:curriculum/output:outputs/output:output[output:conference-poster]">
      <xsl:sort select="output:*/output:publication-year" order="descending"/>
    </xsl:apply-templates>
    <xsl:text>\end{enumerate}

\subsection{Book Chapters}
\begin{enumerate}[leftmargin=*]
</xsl:text>
    <xsl:apply-templates select="curriculum:curriculum/output:outputs/output:output[output:book-chapter]">
      <xsl:sort select="output:*/output:publication-year" order="descending"/>
    </xsl:apply-templates>
    <xsl:text>\end{enumerate}

\section{Services}

<!--
\subsection{Supervisions - PhD}
\begin{enumerate}[leftmargin=*]
</xsl:text>
    <xsl:apply-templates select="curriculum:curriculum/service:services/service:service/service:research-based-degree-supervision[service:degree-type/@code='D']">
      <xsl:sort select="service:start-date/@year" order="descending"/>
    </xsl:apply-templates>
    <xsl:text>\end{enumerate}
-->

\subsection{Master's Supervisions}
\begin{enumerate}[leftmargin=*]
</xsl:text>
    <xsl:apply-templates select="curriculum:curriculum/service:services/service:service/service:research-based-degree-supervision[service:degree-type/@code='M']">
      <xsl:sort select="service:start-date/@year" order="descending"/>
    </xsl:apply-templates>
    <xsl:text>\end{enumerate}

\subsection{Capstone Projects Supervisions}
\begin{enumerate}[leftmargin=*]
</xsl:text>
    <xsl:apply-templates select="curriculum:curriculum/service:services/service:service/service:research-based-degree-supervision[service:degree-type/@code='LB']">
      <xsl:sort select="service:start-date/@year" order="descending"/>
    </xsl:apply-templates>
    <xsl:text>\end{enumerate}

\subsection{Other Supervisions}
\begin{enumerate}[leftmargin=*]
</xsl:text>
    <xsl:apply-templates select="curriculum:curriculum/service:services/service:service[service:mentoring]">
      <xsl:sort select="service:mentoring/service:start-date/@year" order="descending"/>
    </xsl:apply-templates>
    <xsl:text>\end{enumerate}

\subsection{Event Organization}
\begin{enumerate}[leftmargin=*]
</xsl:text>
    <xsl:apply-templates select="curriculum:curriculum/service:services/service:service[service:event-administration]">
      <xsl:sort select="service:*/service:activity-start-date/@year" order="descending"/>
    </xsl:apply-templates>
    <xsl:text>\end{enumerate}

\subsection{Event Participation}
\begin{enumerate}[leftmargin=*]
</xsl:text>
    <xsl:apply-templates select="curriculum:curriculum/service:services/service:service[service:event-participation]">
      <xsl:sort select="service:*/service:activity-start-date/@year" order="descending"/>
    </xsl:apply-templates>
    <xsl:text>\end{enumerate}

\subsection{Teaching}
\begin{enumerate}[leftmargin=*]
</xsl:text>
<xsl:apply-templates select="curriculum:curriculum/service:services/service:service[service:course-taught]">
  <xsl:sort select="service:course-taught/service:start-date/@year" order="descending"/>
  <xsl:sort select="service:course-taught/service:start-date/@month" order="descending"/>
</xsl:apply-templates>
<xsl:text>\end{enumerate}

\subsection{Jury Participation}
\begin{enumerate}[leftmargin=*]
</xsl:text>
    <xsl:apply-templates select="curriculum:curriculum/service:services/service:service[service:graduate-examination]">
      <xsl:sort select="service:*/service:date/@year" order="descending"/>
    </xsl:apply-templates>
    <xsl:text>\end{enumerate}

\section{Distinctions and Awards}
\begin{enumerate}[leftmargin=*]
</xsl:text>
    <xsl:apply-templates select="curriculum:curriculum/distinction:distinctions/distinction:distinction">
      <xsl:sort select="distinction:effective-date" order="descending"/>
    </xsl:apply-templates>
    <xsl:text>\end{enumerate}

\end{document}
</xsl:text>
  </xsl:template>
  
<!-- Helper template to format author names: "First Last" → "F. Last" -->
<xsl:template name="format-author">
  <xsl:param name="author"/>
  
  <xsl:variable name="trimmed" select="normalize-space($author)"/>
  
  <xsl:choose>
    <!-- Format: "Last, First Middle" → "F. Last" -->
    <xsl:when test="contains($trimmed, ',')">
      <xsl:variable name="last" select="normalize-space(substring-before($trimmed, ','))"/>
      <xsl:variable name="first-part" select="normalize-space(substring-after($trimmed, ','))"/>
      <xsl:variable name="first-initial" select="substring($first-part, 1, 1)"/>
      
      <xsl:value-of select="concat($first-initial, '. ', $last)"/>
    </xsl:when>
    
    <!-- Format: "First Middle Last" → "F. Last" -->
    <xsl:otherwise>
      <xsl:variable name="first-initial" select="substring($trimmed, 1, 1)"/>
      
      <!-- Find last word (last name) -->
      <xsl:choose>
        <xsl:when test="contains($trimmed, ' ')">
          <xsl:variable name="last-name">
            <xsl:call-template name="get-last-word">
              <xsl:with-param name="text" select="$trimmed"/>
            </xsl:call-template>
          </xsl:variable>
          <xsl:value-of select="concat($first-initial, '. ', $last-name)"/>
        </xsl:when>
        <xsl:otherwise>
          <xsl:value-of select="$trimmed"/>
        </xsl:otherwise>
      </xsl:choose>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>

<!-- Helper to get last word from a string -->
<xsl:template name="get-last-word">
  <xsl:param name="text"/>
  <xsl:choose>
    <xsl:when test="contains($text, ' ')">
      <xsl:call-template name="get-last-word">
        <xsl:with-param name="text" select="substring-after($text, ' ')"/>
      </xsl:call-template>
    </xsl:when>
    <xsl:otherwise>
      <xsl:value-of select="$text"/>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>

<!-- Unified publications template -->
<xsl:template match="output:output[output:journal-article | output:conference-paper | output:conference-poster | output:book-chapter]">
  <xsl:text>  \item </xsl:text>
  
  <!-- Authors -->
  <xsl:if test="output:*/output:authors">
    <xsl:for-each select="output:*/output:authors/common:author">
      <xsl:variable name="formatted-author">
        <xsl:call-template name="format-author">
          <xsl:with-param name="author" select="."/>
        </xsl:call-template>
      </xsl:variable>
      
      <!-- Check if this is you (adjust the contains check to match your name) -->
      <xsl:choose>
        <xsl:when test="contains(., 'Cruz, R') or (contains(., 'Ricardo') and contains(., 'Cruz'))">
          <xsl:text>\textbf{</xsl:text>
          <xsl:call-template name="escape-latex">
            <xsl:with-param name="text" select="$formatted-author"/>
          </xsl:call-template>
          <xsl:text>}</xsl:text>
        </xsl:when>
        <xsl:otherwise>
          <xsl:call-template name="escape-latex">
            <xsl:with-param name="text" select="$formatted-author"/>
          </xsl:call-template>
        </xsl:otherwise>
      </xsl:choose>
      
      <!-- Separator -->
      <xsl:if test="position() != last()">
        <xsl:text>, </xsl:text>
      </xsl:if>
    </xsl:for-each>
    <xsl:text>. </xsl:text>
  </xsl:if>
  
  <!-- Title -->
  <xsl:text>\textbf{</xsl:text>
  <xsl:call-template name="escape-latex">
    <xsl:with-param name="text" select="output:*/output:article-title | output:*/output:paper-title | output:*/output:chapter-title | output:*/output:title"/>
  </xsl:call-template>
  <xsl:text>}. </xsl:text>
  
  <!-- Venue -->
  <xsl:if test="extra:extra/extra:venue | output:journal-article/output:journal | output:conference-paper/output:proceedings-title | output:conference-poster/output:conference-name">
    <xsl:text>\textit{</xsl:text>
    <xsl:call-template name="escape-latex">
      <xsl:with-param name="text" select="extra:extra/extra:venue | output:journal-article/output:journal | output:conference-paper/output:proceedings-title | output:conference-poster/output:conference-name"/>
    </xsl:call-template>
    <xsl:text>}. </xsl:text>
  </xsl:if>
  
  <!-- Year -->
<!-- Year and Month -->
<xsl:choose>
  <!-- Journal article -->
  <xsl:when test="output:journal-article/output:publication-date">
    <xsl:call-template name="format-month">
      <xsl:with-param name="month" select="output:journal-article/output:publication-date/@month"/>
    </xsl:call-template>
    <xsl:value-of select="output:journal-article/output:publication-date/@year"/>
  </xsl:when>
  <!-- Conference paper -->
  <xsl:when test="output:conference-paper/output:presentation-date">
    <xsl:call-template name="format-month">
      <xsl:with-param name="month" select="output:conference-paper/output:presentation-date/@month"/>
    </xsl:call-template>
    <xsl:value-of select="output:conference-paper/output:presentation-date/@year"/>
  </xsl:when>
  <!-- Conference poster -->
  <xsl:when test="output:conference-poster/output:conference-date">
    <xsl:call-template name="format-month">
      <xsl:with-param name="month" select="output:conference-poster/output:conference-date/@month"/>
    </xsl:call-template>
    <xsl:value-of select="output:conference-poster/output:conference-date/@year"/>
  </xsl:when>
  <!-- Book chapter or fallback -->
  <xsl:otherwise>
    <xsl:value-of select="output:*/output:publication-year"/>
  </xsl:otherwise>
</xsl:choose>
<xsl:text>.</xsl:text>

  <!-- DOI -->
  <xsl:if test="output:*/output:identifiers/output:identifier[output:identifier-type/@code='doi']">
    <xsl:text> DOI: \href{https://doi.org/</xsl:text>
    <xsl:value-of select="output:*/output:identifiers/output:identifier[output:identifier-type/@code='doi']/output:identifier"/>
    <xsl:text>}{</xsl:text>
    <xsl:call-template name="escape-latex">
      <xsl:with-param name="text" select="output:*/output:identifiers/output:identifier[output:identifier-type/@code='doi']/output:identifier"/>
    </xsl:call-template>
    <xsl:text>}</xsl:text>
  </xsl:if>
  
  <xsl:text>
</xsl:text>
</xsl:template>

<!-- Helper template to format month -->
<xsl:template name="format-month">
  <xsl:param name="month"/>
  <xsl:if test="$month">
    <xsl:choose>
      <xsl:when test="$month='01'">Jan</xsl:when>
      <xsl:when test="$month='02'">Feb</xsl:when>
      <xsl:when test="$month='03'">Mar</xsl:when>
      <xsl:when test="$month='04'">Apr</xsl:when>
      <xsl:when test="$month='05'">May</xsl:when>
      <xsl:when test="$month='06'">Jun</xsl:when>
      <xsl:when test="$month='07'">Jul</xsl:when>
      <xsl:when test="$month='08'">Aug</xsl:when>
      <xsl:when test="$month='09'">Sep</xsl:when>
      <xsl:when test="$month='10'">Oct</xsl:when>
      <xsl:when test="$month='11'">Nov</xsl:when>
      <xsl:when test="$month='12'">Dec</xsl:when>
    </xsl:choose>
  </xsl:if>
</xsl:template>

  <!-- Services templates -->
  <xsl:template match="service:research-based-degree-supervision">
    <xsl:text>  \item \textbf{</xsl:text>
    <xsl:call-template name="escape-latex">
      <xsl:with-param name="text" select="service:student-name"/>
    </xsl:call-template>
    <xsl:text>}</xsl:text>
    <xsl:if test="service:degree-status/@code='EC'">
      <xsl:text> (Ongoing)</xsl:text>
    </xsl:if>
    <xsl:text>. \textit{</xsl:text>
    <xsl:call-template name="escape-latex">
      <xsl:with-param name="text" select="service:thesis-title"/>
    </xsl:call-template>
    <xsl:text>}. </xsl:text>
    <xsl:value-of select="service:start-date/@year"/>
    <xsl:if test="service:end-date/@year">
      <xsl:text>/</xsl:text>
      <xsl:value-of select="service:end-date/@year"/>
    </xsl:if>
    <xsl:if test="not(service:end-date/@year)">
      <xsl:text>/Present</xsl:text>
    </xsl:if>
    <xsl:text>. </xsl:text>
    <xsl:call-template name="escape-latex">
      <xsl:with-param name="text" select="service:academic-institutions/common:institution/common:institution-name"/>
    </xsl:call-template>
    <xsl:text>.
</xsl:text>
  </xsl:template>

<!-- Mentoring/Tutoring template -->
<xsl:template match="service:service[service:mentoring]">
  <xsl:text>  \item \textbf{</xsl:text>
  <xsl:call-template name="escape-latex">
    <xsl:with-param name="text" select="service:mentoring/service:name-of-protege"/>
  </xsl:call-template>
  <xsl:text>}</xsl:text>
  <xsl:text>. \textit{</xsl:text>
  <xsl:call-template name="escape-latex">
    <xsl:with-param name="text" select="service:mentoring/service:topic-of-mentor-ship"/>
  </xsl:call-template>
  <xsl:text>}. </xsl:text>
  
  <!-- Check if start and end are the same -->
  <xsl:choose>
    <!-- Same month and year: show only once -->
    <xsl:when test="service:mentoring/service:end-date/@year = service:mentoring/service:start-date/@year and service:mentoring/service:end-date/@month = service:mentoring/service:start-date/@month">
      <xsl:call-template name="format-month">
        <xsl:with-param name="month" select="service:mentoring/service:end-date/@month"/>
      </xsl:call-template>
      <xsl:text>/</xsl:text>
      <xsl:value-of select="service:mentoring/service:end-date/@year"/>
    </xsl:when>
    
    <!-- Different dates: show range -->
    <xsl:otherwise>
      <!-- Start date with month -->
      <xsl:call-template name="format-month">
        <xsl:with-param name="month" select="service:mentoring/service:start-date/@month"/>
      </xsl:call-template>
      <xsl:text>/</xsl:text>
      <xsl:value-of select="service:mentoring/service:start-date/@year"/>
      
      <!-- End date with month if exists -->
      <xsl:if test="service:mentoring/service:end-date/@year">
        <xsl:text>--</xsl:text>
        <xsl:call-template name="format-month">
          <xsl:with-param name="month" select="service:mentoring/service:end-date/@month"/>
        </xsl:call-template>
        <xsl:text>/</xsl:text>
        <xsl:value-of select="service:mentoring/service:end-date/@year"/>
      </xsl:if>
    </xsl:otherwise>
  </xsl:choose>
  
  <xsl:text>. </xsl:text>
  <xsl:if test="service:mentoring/service:description">
    <xsl:call-template name="escape-latex">
      <xsl:with-param name="text" select="service:mentoring/service:description"/>
    </xsl:call-template>
    <xsl:text>.</xsl:text>
  </xsl:if>
  <xsl:text>
</xsl:text>
</xsl:template>

<xsl:template match="service:service[service:event-administration | service:event-participation]">
  <xsl:text>  \item \textbf{</xsl:text>
  <xsl:call-template name="escape-latex">
    <xsl:with-param name="text" select="service:event-administration/service:event-description | service:event-participation/service:event-description"/>
  </xsl:call-template>
  <xsl:text>}</xsl:text>
  
  <!-- Event name (for participation) -->
  <xsl:if test="service:event-participation/service:event-name">
    <xsl:text>. </xsl:text>
    <xsl:call-template name="escape-latex">
      <xsl:with-param name="text" select="service:event-participation/service:event-name"/>
    </xsl:call-template>
  </xsl:if>
  
  <xsl:text> (</xsl:text>
  
  <!-- Date -->
  <xsl:choose>
    <xsl:when test="service:event-administration">
      <xsl:call-template name="format-month">
        <xsl:with-param name="month" select="service:event-administration/service:event-start-date/@month"/>
      </xsl:call-template>
      <xsl:value-of select="service:event-administration/service:event-start-date/@year"/>
    </xsl:when>
    <xsl:when test="service:event-participation">
      <xsl:value-of select="service:event-participation/service:start-date/@day"/>
      <xsl:text> </xsl:text>
      <xsl:call-template name="format-month">
        <xsl:with-param name="month" select="service:event-participation/service:start-date/@month"/>
      </xsl:call-template>
      <xsl:value-of select="service:event-participation/service:start-date/@year"/>
    </xsl:when>
  </xsl:choose>
  
  <xsl:text>)</xsl:text>
  
  <!-- Role (if exists) -->
  <xsl:if test="service:event-administration/service:administrative-role">
    <xsl:text>. Role: </xsl:text>
    <xsl:value-of select="service:event-administration/service:administrative-role"/>
  </xsl:if>
  
  <xsl:text>.
</xsl:text>
</xsl:template>

<xsl:template match="service:service[service:graduate-examination]">
  <xsl:text>  \item \textbf{</xsl:text>
  <xsl:call-template name="escape-latex">
    <xsl:with-param name="text" select="service:graduate-examination/service:theme"/>
  </xsl:call-template>
  <xsl:text>}. Student: </xsl:text>
  <xsl:call-template name="escape-latex">
    <xsl:with-param name="text" select="service:graduate-examination/service:student-name"/>
  </xsl:call-template>
  <xsl:text>. </xsl:text>
  
  <!-- Day Month Year -->
  <xsl:value-of select="service:graduate-examination/service:date/@day"/>
  <xsl:text>/</xsl:text>
  <xsl:call-template name="format-month">
    <xsl:with-param name="month" select="service:graduate-examination/service:date/@month"/>
  </xsl:call-template>
  <xsl:text>/</xsl:text>
  <xsl:value-of select="service:graduate-examination/service:date/@year"/>
  
  <xsl:text>. Role: </xsl:text>
  <xsl:value-of select="service:graduate-examination/service:examination-role"/>
  <xsl:text>.
</xsl:text>
</xsl:template>

  <!-- Distinctions template -->
  <xsl:template match="distinction:distinction">
    <xsl:text>  \item \textbf{</xsl:text>
    <xsl:call-template name="escape-latex">
      <xsl:with-param name="text" select="distinction:distinction-name"/>
    </xsl:call-template>
    <xsl:text>} (</xsl:text>
    <xsl:value-of select="distinction:effective-date"/>
    <xsl:text>)</xsl:text>
    <xsl:if test="distinction:description">
      <xsl:text>. </xsl:text>
      <xsl:call-template name="escape-latex">
        <xsl:with-param name="text" select="distinction:description"/>
      </xsl:call-template>
    </xsl:if>
    <xsl:text>.
</xsl:text>
  </xsl:template>

  <!-- LaTeX escape template -->
  <xsl:template name="escape-latex">
    <xsl:param name="text"/>
    <xsl:variable name="amp">&amp;</xsl:variable>
    <xsl:variable name="bs">\</xsl:variable>
    <xsl:call-template name="string-replace">
      <xsl:with-param name="text">
        <xsl:call-template name="string-replace">
          <xsl:with-param name="text">
            <xsl:call-template name="string-replace">
              <xsl:with-param name="text">
                <xsl:call-template name="string-replace">
                  <xsl:with-param name="text" select="$text"/>
                  <xsl:with-param name="from" select="$bs"/>
                  <xsl:with-param name="to">\textbackslash{}</xsl:with-param>
                </xsl:call-template>
              </xsl:with-param>
              <xsl:with-param name="from" select="$amp"/>
              <xsl:with-param name="to">\&amp;</xsl:with-param>
            </xsl:call-template>
          </xsl:with-param>
          <xsl:with-param name="from">%</xsl:with-param>
          <xsl:with-param name="to">\%</xsl:with-param>
        </xsl:call-template>
      </xsl:with-param>
      <xsl:with-param name="from">_</xsl:with-param>
      <xsl:with-param name="to">\_</xsl:with-param>
    </xsl:call-template>
  </xsl:template>

<!-- Courses Taught template -->
<xsl:template match="service:service[service:course-taught]">
  <xsl:text>  \item \textbf{</xsl:text>
  <xsl:call-template name="escape-latex">
    <xsl:with-param name="text" select="service:course-taught/service:academic-session"/>
  </xsl:call-template>
  <xsl:text>}</xsl:text>
  <xsl:text> (</xsl:text>
  <xsl:call-template name="escape-latex">
    <xsl:with-param name="text" select="service:course-taught/service:course-title"/>
  </xsl:call-template>
  <xsl:text>). </xsl:text>
  
  <!-- Start month/year -->
  <xsl:call-template name="format-month">
    <xsl:with-param name="month" select="service:course-taught/service:start-date/@month"/>
  </xsl:call-template>
  <xsl:text>/</xsl:text>
  <xsl:value-of select="service:course-taught/service:start-date/@year"/>
  
  <xsl:text>--</xsl:text>
  
  <!-- End month/year -->
  <xsl:call-template name="format-month">
    <xsl:with-param name="month" select="service:course-taught/service:end-date/@month"/>
  </xsl:call-template>
  <xsl:text>/</xsl:text>
  <xsl:value-of select="service:course-taught/service:end-date/@year"/>
  
  <xsl:text>. </xsl:text>
  <xsl:call-template name="escape-latex">
    <xsl:with-param name="text" select="service:course-taught/common:institutions/common:institution/common:institution-name"/>
  </xsl:call-template>
  <xsl:text>.
</xsl:text>
</xsl:template>

  <!-- String replace utility -->
  <xsl:template name="string-replace">
    <xsl:param name="text"/>
    <xsl:param name="from"/>
    <xsl:param name="to"/>
    <xsl:choose>
      <xsl:when test="contains($text, $from)">
        <xsl:value-of select="substring-before($text, $from)"/>
        <xsl:value-of select="$to"/>
        <xsl:call-template name="string-replace">
          <xsl:with-param name="text" select="substring-after($text, $from)"/>
          <xsl:with-param name="from" select="$from"/>
          <xsl:with-param name="to" select="$to"/>
        </xsl:call-template>
      </xsl:when>
      <xsl:otherwise>
        <xsl:value-of select="$text"/>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

</xsl:stylesheet>
