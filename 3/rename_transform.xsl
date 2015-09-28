<xsl:stylesheet version="1.0"
      xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:template match="@*|node()">
    <xsl:copy>
        <xsl:apply-templates select="@*|node()" />
    </xsl:copy>
</xsl:template>

<!--Rename tags-->
<xsl:template match="maxKbps">
    <maxSpeed>
      <xsl:apply-templates select="@*|node()" />
    </maxSpeed>
</xsl:template>

<xsl:template match="feed">
    <feedTag>
      <xsl:apply-templates select="@*|node()" />
    </feedTag>
</xsl:template>

<!--Rename attributes-->
<xsl:template match="@label">
   <xsl:attribute name="text">
      <xsl:value-of select="."/>
   </xsl:attribute>
</xsl:template>

<xsl:template match="@marketID">
   <xsl:attribute name="marketType">
      <xsl:value-of select="."/>
   </xsl:attribute>
</xsl:template>

</xsl:stylesheet>